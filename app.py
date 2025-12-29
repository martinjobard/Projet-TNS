from datetime import datetime, date
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, url_for, session, redirect, g, Response, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import sqlite3
import os
import unicodedata
import json
import csv
import io
app = Flask(__name__)
# Vous avez besoin d'une clé secrète pour les sessions (TRÈS IMPORTANT !)
app.config['SECRET_KEY'] = 'ma_cle_secrete_tres_sure_a_changer'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/images/profiles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Définition du Gardien ---
def require_login():
    if 'logged_in' not in session:
        return redirect(url_for('Connexion')) 
    return None

def allowed_file(filename):
    # 1. Vérifie si le nom de fichier contient un point
    # 2. Sépare le nom au dernier point (rsplit('.', 1)) et met l'extension en minuscules
    # 3. Vérifie si cette extension fait partie de notre ensemble ALLOWED_EXTENSIONS
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- Fonctions de Routes Protégées ---
DATABASE= "gestion_projets_test.db"


def get_db(): # cette fonction permet de créer une connexion à la base 
              # ou de récupérer la connexion existante 
    if 'db' not in g:  # plus propre que getattr()
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # très important !
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    # Récupère l'objet 'db' de 'g' et le supprime (s'il existe)
    db = g.pop('db', None) 
    if db is not None:
        db.close()

# Fonction utilitaire pour trouver les coordonnées
def geocode_adresse(adresse_texte):
    try:
        # IMPORTANT : Tu dois donner un nom unique à user_agent (ex: le nom de ton projet)
        # Sinon OpenStreetMap bloquera tes requêtes.
        geolocator = Nominatim(user_agent="TNS_Gestion_App_V1")
        
        location = geolocator.geocode(adresse_texte, timeout=10)
        
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Erreur de géocodage : {e}")
        return None, None


@app.route('/')
def Accueil():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    titer_page_actuelle = "Accueil"
    username = session.get('username')
    db = get_db()
    c = db.cursor()
    sql_data = "SELECT I.role FROM Utilisateur_Intervenant UI LEFT JOIN Intervenants I ON UI.idi = I.idi WHERE UI.nom_utilisateur = ?"
    c.execute(sql_data, (username,))
    role_data = c.fetchone()
    if role_data:
        role = role_data['role']
    sql_clients_projets = "SELECT C.nom, C.prenom, P.titre_projet, P.etat FROM Clients C LEFT JOIN Projets P ON C.idc = P.idc"
    c.execute(sql_clients_projets)
    clients_data = c.fetchall()
    clients_dict = {}
    for row in clients_data:
        nom_complet = f"{row['nom']}.{row['prenom']}"
        if nom_complet not in clients_dict:
            clients_dict[nom_complet] = []
        if row['titre_projet']:
            clients_dict[nom_complet].append({
                "titre_projet": row['titre_projet'],
                "etat": row['etat']
            })
    return render_template('Accueil.html', titre=titre_site, titre_page_actuelle=titer_page_actuelle, username=username, role=role, clients=clients_dict)

@app.route('/Clients')
def Clients():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    titre_page_actuelle = "Clients"
    return render_template('Clients.html', titre=titre_site, titre_page_actuelle=titre_page_actuelle)

@app.route('/Projets')
def Projets():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    titre_page_actuelle = "Projets"

    db=get_db()
    sql="""
    SELECT p.idp, p.etat, c.nom as client_nom, p.budget, p.deb, p.fin, p.titre_projet 
    FROM Projets p LEFT JOIN Clients c ON p.idc=c.idc
    """
    liste_projets=db.execute(sql).fetchall()
    liste_en_cours=[p for p in liste_projets if p['etat']=='En cours']
    liste_termines=[p for p in liste_projets if p['etat']=='Terminé']
    liste_en_attente=[p for p in liste_projets if p['etat']=='En attente']
    return render_template('Projets.html', titre=titre_site, titre_page_actuelle=titre_page_actuelle, tous_les_projets=liste_projets, 
                           projets_en_cours=liste_en_cours, projets_termines=liste_termines, projets_attente=liste_en_attente)

@app.route('/details_projet/<int:id_projet>')
def details_projet(id_projet):
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    
    db = get_db()
    sql_projet="SELECT p.*, c.nom_entreprise, c.nom as nom_client, c.prenom as prenom_client FROM Projets p LEFT JOIN Clients c ON p.idc=c.idc WHERE p.idp=?"
    projet=db.execute(sql_projet, (id_projet,)).fetchone()

    if not projet :
        return "Projet introuvable"
    
    sql_docs="SELECT * FROM Documents WHERE idp=?"
    documents=db.execute(sql_docs, (id_projet,)).fetchall()

    sql_equipe="SELECT i.nom, i.prenom, i.idi FROM Intervenants i JOIN Participation pa ON i.idi = pa.idi WHERE pa.idp = ?"
    equipe=db.execute(sql_equipe, (id_projet,)).fetchall()

    candidats_suggeres=algorythme_matching(id_projet)
    return render_template('details_projet.html', p=projet, docs=documents, candidats=candidats_suggeres, equipe=equipe)


@app.route('/Intervenants')
def Intervenants():

    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    
    db = get_db()
    c = db.cursor()
    titre_site = "Site interne TNS"
    titre_page_actuelle = "Intervenants"
    
    rows=[]
    sql="SELECT nom, prenom FROM Intervenants "
    c.execute(sql)
    rows = c.fetchall()

    nom_affiche = normalize_text(rows[0]['nom'])
    prenom_affiche = normalize_text(rows[0]['prenom'])
    
    intervenants = []
    for row in rows:
        nom=row["nom"]
        prenom=row["prenom"]
        lien=f"{nom}.{prenom}"
        intervenants.append({
            
            "nom": nom, 
            "prenom":prenom , 
            "lien": lien
        })

    


# FELICITER LA OU LES DEUX PERSONNES QUI ONT REALISE LE PLUS DE PROJET 
    sql1="""
    SELECT nom, prenom, COUNT(Participation.idi) as nb_projets
    FROM Intervenants
    LEFT JOIN Participation ON Intervenants.idi = Participation.idi
    LEFT JOIN Projets ON Projets.idp=Participation.idp
    GROUP BY nom, prenom
    ORDER BY nb_projets DESC
    LIMIT 3  
    """
    c.execute(sql1)
    
    top_3 = c.fetchall()
    

    if len(top_3) > 0:
    
    # Le meilleur score 
        score_max = top_3[0][2] 
    
    # On compte combien de gens ont ce score max dans notre liste de 3
    # (On crée une liste temporaire avec tous les gagnants ex-aequo)
    gagnants = [p for p in top_3 if p[2] == score_max]
    
    nb_gagnants = len(gagnants)
        
    if nb_gagnants == 1:
        
        p = gagnants[0]
        honors1 = [f"{p[0]} {p[1]} qui a réalisé {p[2]} projets"]
        
    elif nb_gagnants == 2:
        p1 = gagnants[0]
        p2 = gagnants[1]
        honors1=[]
        honors1.append(f"{p1[0]} {p1[1]} et {p2[0]} {p2[1]} ({p1[2]} projets)")
        
    else: 
       pass 

# ACCUEILLIR LES NOUVEAUX INSCRITS À TNS
    sql2="""
    SELECT nom, prenom, date_inscription
    FROM Intervenants
    ORDER BY date_inscription DESC
    LIMIT 3  
    """

    c.execute(sql2)
    top_3 = c.fetchall()
    

    if len(top_3) > 0:
    
    # Le meilleur score 
        date_min = top_3[0][2] 
    
    # On compte combien de gens ont ce score max dans notre liste de 3
    # (On crée une liste temporaire avec tous les gagnants ex-aequo)
    gagnants = [p for p in top_3 if p[2] == date_min]
    
    nb_gagnants = len(gagnants)
        
    if nb_gagnants == 1:
        
        p = gagnants[0]
        honors2 = [f"{p[0]} {p[1]}"]
        
    elif nb_gagnants == 2:
        p1 = gagnants[0]
        p2 = gagnants[1]
        honors2=[]
        honors2.append(f"{p1[0]} {p1[1]} et {p2[0]} {p2[1]} ")
        
    else: 
       pass  
  
#BON COURAGE POUR LE PROJET QUI VIENT DE SE FINIR
    sql3="""SELECT Intervenants.nom, Intervenants.prenom 
    FROM Intervenants 
    LEFT JOIN Participation ON Intervenants.idi = Participation.idi 
    WHERE Participation.idp = (
    
    SELECT idp FROM Projets WHERE fin='' 
    ORDER BY deb DESC 
    LIMIT 1)
    
    """
    c.execute(sql3)
    honors3sql = c.fetchall()
    honors3=[]
    for row in honors3sql:
        nom=row[0]
        prenom=row[1]
        membre=f"{nom} {prenom}"
        honors3.append(membre)

 
#les intervenants sur le projet qui s'est fini ya le moins longtemps

    sql4="""SELECT Intervenants.nom, Intervenants.prenom 
    FROM Intervenants 
    LEFT JOIN Participation ON Intervenants.idi = Participation.idi 
    WHERE Participation.idp = (
    
    SELECT idp FROM Projets 
    ORDER BY fin  
    LIMIT 1)
    """
    c.execute(sql4)
    honors4sql=c.fetchall()
    honors4=[]
    
    for row in honors4sql:
        nom=row[0]
        prenom=row[1]
        membre=f"{nom} {prenom}"
        honors4.append(membre)



    return render_template('Intervenants.html', titre=titre_site,
                            titre_page_actuelle=titre_page_actuelle, intervenants=intervenants, 
                            honors1=honors1, honors2=honors2, honors3=honors3,
                            honors4=honors4)

@app.route('/Import-Export')
def Import_Export():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    
    db = get_db() # ⬅️ Connexion à la BDD
    cursor = db.cursor()
    
    # Exécution de la requête pour obtenir tous les clients
    sql = "SELECT idc, nom, prenom FROM Clients"
    liste_clients = cursor.execute(sql).fetchall() # Récupère toutes les lignes
    titre_site = "Site interne TNS"
    titre_page_actuelle = "Import-Export"
    return render_template('Import_Export.html', 
                           titre=titre_site, 
                           titre_page_actuelle=titre_page_actuelle,
                           liste_clients=liste_clients)

@app.route('/save_swipe', methods=['POST'])
def save_swipe():
    if 'username' not in session:
        return jsonify({'status': 'error'}), 403

    data = request.get_json()
    client_id = data.get('client_id')
    action = data.get('action') # 'like' ou 'dislike'

    db = get_db()
    username = session['username']
    
    sql_user = "SELECT idi FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?"
    user_data = db.execute(sql_user, (username,)).fetchone()

    if not user_data:
        return redirect(url_for('logout'))
    
    mon_idi = user_data['idi']
    
    today = date.today().isoformat()

    if action == 'like':
        sql_exist = "SELECT 1 FROM Historique WHERE idc = ? AND interaction_text = 'TINDER_LIKE'"
        exist = db.execute(sql_exist, (client_id,)).fetchone()
        if not exist:
            sql_not_exist = "INSERT INTO Historique (date, idc, idi, interaction_text) VALUES (?, ?, ?, 'TINDER_LIKE')"
            db.execute(sql_not_exist, (today, client_id, mon_idi))
            db.commit()
            return jsonify({'status': 'success'})
    
    elif action == 'dislike':
        sql_dislike = "INSERT INTO Historique (date, idc, idi, interaction_text) VALUES (?, ?, ?, 'TINDER_DISLIKE')"
        db.execute(sql_dislike, (today, client_id, mon_idi))
        db.commit()
        return jsonify({'status': 'success'})

    return jsonify({'status': 'error'})

@app.route('/annuler_match/<int:client_id>', methods=['POST'])
def annuler_match(client_id):
    if 'username' not in session:
        return redirect(url_for('Connexion'))

    db = get_db()
    username = session['username']

    sql_user = "SELECT idi FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?"
    user_data = db.execute(sql_user, (username,)).fetchone()

    if not user_data:
        return redirect(url_for('logout'))
    
    mon_idi = user_data['idi']
    
    sql_annuler_match = "DELETE FROM Historique WHERE idc = ? AND idi = ? AND interaction_text = 'TINDER_LIKE'"
    db.execute(sql_annuler_match,(client_id, mon_idi))
    db.commit()

    return redirect(url_for('tinder_like'))

@app.route('/reset_dislikes')
def reset_dislikes():
    if 'username' not in session:
        return redirect(url_for('Connexion'))
    
    db = get_db()
    username = session['username']
    
    sql_user = "SELECT idi FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?"
    user_data = db.execute(sql_user, (username,)).fetchone()

    if not user_data:
        return redirect(url_for('logout'))
    
    mon_idi = user_data['idi']

    sql_reset_dislike = "DELETE FROM Historique WHERE idi = ? AND interaction_text = 'TINDER_DISLIKE'"
    db.execute(sql_reset_dislike, (mon_idi,))
    db.commit()

    return redirect(url_for('tinder_like'))

@app.route('/tinder_like')
def tinder_like():
    redirect_if_needed = require_login()
    if redirect_if_needed: return redirect_if_needed
    
    titre_site = "Prospection TNS"
    db = get_db()
    
    username = session['username']
    user_data = db.execute("SELECT idi FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?", (username,)).fetchone()
    if not user_data: return redirect(url_for('logout'))
    mon_idi = user_data['idi']
    
    attribution_finale = {}

    sql_projets = "SELECT P.idp, P.idc, P.titre_projet, C.nom_entreprise, C.secteur FROM Projets P LEFT JOIN Clients C ON P.idc = C.idc WHERE P.etat = 'En attente'"
    tous_les_projets = db.execute(sql_projets).fetchall()

    for projet in tous_les_projets:
        projet_id = projet['idp']
        client_id = projet['idc']
        est_deja_pris_sql = "SELECT 1 FROM Historique WHERE idc = ? AND interaction_text = 'TINDER_LIKE'"
        est_deja_pris = db.execute(est_deja_pris_sql,(client_id,)).fetchone()
        if est_deja_pris:
            continue 

        classement = algorythme_matching(projet_id) 
        
        candidat_retenu = None
        score_retenu = 0

        for candidat in classement:
            candidat_idi = candidat['idi']
            
            # Vérifie si Dislike
            a_refuse_sql = "SELECT 1 FROM Historique WHERE idc = ? AND idi = ? AND interaction_text = 'TINDER_DISLIKE'"
            a_refuse = db.execute(a_refuse_sql, (client_id, candidat_idi)).fetchone()
            if not a_refuse:
                candidat_retenu = candidat_idi
                score_retenu = candidat['score']
                break 
        
        # Si le client a plusieurs projets en attente
        if candidat_retenu:
            if client_id not in attribution_finale:
                attribution_finale[client_id] = {
                    'gagnant_idi': candidat_retenu,
                    'score': score_retenu,
                    'info_client': projet 
                }
            else:
                # On garde le projet qui rapporte le plus de points
                if score_retenu > attribution_finale[client_id]['score']:
                    attribution_finale[client_id] = {
                        'gagnant_idi': candidat_retenu,
                        'score': score_retenu,
                        'info_client': projet
                    }
    
    cartes_proposées = []
    
    for cid, data in attribution_finale.items():
        if data['gagnant_idi'] == mon_idi:
            projet_info = data['info_client']
            cartes_proposées.append({
                'id': cid,
                'nom': projet_info['nom_entreprise'],
                'secteur': projet_info['secteur'],
                'projet_concerne': projet_info['titre_projet']
            })

    sql_potentiels_clients = "SELECT Clients.idc, Clients.nom_entreprise, Clients.secteur, Clients.email, Clients.telephone FROM Clients LEFT JOIN Historique ON Clients.idc = Historique.idc WHERE Historique.idi = ? AND Historique.interaction_text = 'TINDER_LIKE'"
    potentiels_clients = db.execute(sql_potentiels_clients, (mon_idi,)).fetchall()

    return render_template(
        'tinder_like.html', 
        titre=titre_site, 
        titre_page_actuelle="Tinder Like",
        clients=cartes_proposées,
        mes_clients=potentiels_clients
    )

@app.route('/Stats')
def Stats():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    
    db = get_db()
    
    username = session['username']
    sql_user = "SELECT idi FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?"
    user_data = db.execute(sql_user, (username,)).fetchone()
    
    if not user_data:
        return redirect(url_for('logout'))
    
    mon_idi = user_data['idi']
    sql_tous = "SELECT idi, nom, prenom FROM Intervenants ORDER BY nom"
    tous_les_intervenants = db.execute(sql_tous).fetchall()

    target_idi = request.args.get('target_idi')
    
    if target_idi == 'all':
        id_a_analyser = 'all'
    elif target_idi:
        try:
            id_a_analyser = int(target_idi)
        except ValueError:
            id_a_analyser = mon_idi 
    else:
        id_a_analyser = mon_idi

    selected_year = request.args.get('year')
    if selected_year == 'all':
        selected_year = None 
    
    conditions = []
    params_base = []

    if id_a_analyser != 'all':
        conditions.append("Participation.idi = ?") 
        params_base.append(id_a_analyser)

    if selected_year:
        conditions.append("substr(Projets.deb, 7, 4) = ?")
        params_base.append(selected_year)

    sql_where = "WHERE " + " AND ".join(conditions) if conditions else ""

    sql_nb_projets = f"SELECT COUNT(DISTINCT Projets.idp) FROM Projets LEFT JOIN Participation ON Projets.idp=Participation.idp {sql_where}"
    nb_projects = db.execute(sql_nb_projets, params_base).fetchone()[0]

    sql_nb_clients = f"SELECT COUNT(DISTINCT Projets.idc) FROM Projets LEFT JOIN Participation ON Projets.idp=Participation.idp {sql_where}"
    nb_clients = db.execute(sql_nb_clients, params_base).fetchone()[0]

    sql_mois = f"SELECT substr(Projets.deb, 4, 2) as mois, COUNT(DISTINCT Projets.idp) as nombre FROM Projets LEFT JOIN Participation ON Projets.idp = Participation.idp {sql_where} GROUP BY mois"
    resultats_mois = db.execute(sql_mois, params_base).fetchall()
    
    projets_par_mois = [0] * 12
    for row in resultats_mois:
        if row['mois']:
            try:
                index = int(row['mois']) - 1
                if 0 <= index < 12: projets_par_mois[index] = row['nombre']
            except: pass

    sql_table = f"SELECT nom_entreprise, secteur, etat, deb, role FROM Clients LEFT JOIN Projets ON Clients.idc=Projets.idc LEFT JOIN Participation ON Projets.idp=Participation.idp {sql_where}"
    table_raw = db.execute(sql_table, params_base).fetchall()

    sql_pie = f"SELECT Clients.secteur, COUNT(DISTINCT Projets.idp) as nombre FROM Clients LEFT JOIN Projets ON Clients.idc = Projets.idc LEFT JOIN Participation ON Projets.idp = Participation.idp {sql_where} GROUP BY Clients.secteur"
    pie_raw = db.execute(sql_pie, params_base).fetchall()

    liste_labels = [row['secteur'] for row in pie_raw]
    liste_values = [row['nombre'] for row in pie_raw]
    
    table_data = []
    for line in table_raw:
        role = line['role']
        if role is None:
            role = "Indéfini"
        date = line['deb']
        if date == "":
            date = "Indéfinie"
        table_data.append({
            "client": line['nom_entreprise'],
            "sector": line['secteur'],
            "role": role,
            "status": line['etat'],
            "date": date
        })

    return render_template(
        "Stats.html",
        nb_clients=nb_clients, 
        nb_projects=nb_projects,
        monthly_labels=["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
        monthly_projects=projets_par_mois,
        sector_labels=liste_labels, 
        sector_values=liste_values,
        table_data=table_data,
        intervenants=tous_les_intervenants,
        selected_id=id_a_analyser,
        selected_year=selected_year if selected_year else 'all' 
    )

@app.route('/Missions_réalisées')
def Missions_réalisées():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed 
    titre_site = "Site interne TNS"

    db=get_db()
    sql = """SELECT p.idp, p.etat, c.nom as client_nom, p.budget, p.deb, p.fin, p.titre_projet, d.chemin as doc_ul, GROUP_CONCAT(DISTINCT d.chemin) as docs
    FROM Projets p LEFT JOIN Clients c ON p.idc=c.idc LEFT JOIN Documents d ON p.idp=d.idp GROUP BY p.idp"""
    liste_projets=db.execute(sql).fetchall()
    missions_finies=[p for p in liste_projets if p['etat']=='Terminé']
    titre_page_actuelle = "Missions Réalisées"
    return render_template('Missions_réalisées.html', titre=titre_site, titre_page_actuelle=titre_page_actuelle, projets=missions_finies)




@app.route('/Partenaires')
def Partenaires():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    titre_page_actuelle = "Partenaires"
    return render_template('Partenaires.html', titre=titre_site, titre_page_actuelle=titre_page_actuelle)

@app.route('/Contact')
def Contact():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    titre_page_actuelle = "Contact"
    return render_template('Contact.html', titre=titre_site, titre_page_actuelle=titre_page_actuelle)

@app.route('/Mon_compte')
def Mon_compte():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    
    username = session.get('username')
    
    # On utilise ta fonction get_db() qui est plus propre
    db = get_db()
    c = db.cursor()

    # --- LA REQUÊTE AVEC JOINTURE ---
    # On récupère les infos du compte ET les infos de l'intervenant lié par l'idi
    sql = """
    SELECT 
        UI.nom_utilisateur, 
        UI.email_utilisateur, 
        UI.pdp_url, 
        UI.fonction,
        I.nom, 
        I.prenom,
        I.dispo
    FROM Utilisateur_Intervenant UI
    JOIN Intervenants I ON UI.idi = I.idi 
    WHERE UI.nom_utilisateur = ?
    """
    
    c.execute(sql, (username,))
    data = c.fetchone()

    # On joint Projets, Participation et Utilisateur_Intervenant pour recuperer les missions
    sql_missions = """
    SELECT 
        P.titre_projet, 
        P.etat, 
        P.deb, 
        P.fin, 
        Pa.role 
    FROM Projets P
    JOIN Participation Pa ON P.idp = Pa.idp
    JOIN Utilisateur_Intervenant UI ON Pa.idi = UI.idi
    WHERE UI.nom_utilisateur = ?
    ORDER BY P.deb DESC
    """
    c.execute(sql_missions, (username,))
    missions_data = c.fetchall() # On récupère toutes les lignes (liste de missions)

    # Initialisation des variables
    nom_compte = "Inconnu"
    email = "Inconnu"
    pdp_url = None
    lien_formatte = None # C'est la variable pour ton URL
    fonction_recuperee = ""

    if data:
        # 1. Infos du compte utilisateur
        nom_compte = (data['nom_utilisateur'])
        email = data['email_utilisateur']
        pdp_url = data['pdp_url']
        dispo_actuelle = data['dispo']
        fonction_recuperee = data['fonction']
        
        # 2. Infos de l'intervenant pour construire le lien
        # On vérifie que les champs existent bien
        if data['nom'] and data['prenom']:
            nom_reel = normalize_text(data['nom'])
            prenom_reel = normalize_text(data['prenom'])
            # On formate : "Nom.Prenom" pour que la route Inter_profil puisse faire le split('.')
            lien_formatte = f"{nom_reel}.{prenom_reel}"
    titre_page_actuelle = "Mon Compte"
    return render_template('Mon_compte.html', 
        nom_utilisateur=nom_compte, 
        email_utilisateur=email,
        pdp_actuelle=pdp_url,
        lien_intervenant=lien_formatte,
        liste_missions=missions_data,
        dispo=dispo_actuelle,
        titre_page_actuelle=titre_page_actuelle,
        fonction_utilisateur=fonction_recuperee
    )

# --- NOUVELLES ROUTES ---

@app.route('/modifier_disponibilite', methods=['POST'])
def modifier_disponibilite():
    if not session.get('username'):
        return redirect(url_for('login'))

    username = session.get('username')
    nouvelle_dispo = request.form.get('dispo') # Sera 'Oui' ou 'Non'

    db = get_db()
    c = db.cursor()

    try:
        # On met à jour la table Intervenants en passant par la table de liaison
        sql_update = """
        UPDATE Intervenants
        SET dispo = ?
        WHERE idi = (
            SELECT idi FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?
        )
        """
        c.execute(sql_update, (nouvelle_dispo, username))
        db.commit()
        # Optionnel : Ajouter un message flash
        # flash("Disponibilité mise à jour !", "success")
    except Exception as e:
        db.rollback()
        print(f"Erreur update dispo: {e}")

    return redirect(url_for('Mon_compte'))

@app.route('/modifier_nom_email', methods=['POST'])
def modifier_nom_email():
    if 'logged_in' not in session:
        return redirect(url_for('Connexion'))
    
    nouveau_nom = request.form['nom']
    nouvel_email = request.form['email']
    username_actuel = session['username']

    try:
        db = sqlite3.connect(DATABASE)
        c = db.cursor()
        # Mise à jour
        sql = "UPDATE Utilisateur_Intervenant SET nom_utilisateur = ?, email_utilisateur = ? WHERE nom_utilisateur = ?"
        c.execute(sql, (nouveau_nom, nouvel_email, username_actuel))
        db.commit()
        db.close()

        # IMPORTANT : Mettre à jour la session si le nom change
        session['username'] = nouveau_nom
    except Exception as e:
        print(f"Erreur update profil: {e}")
    
    return redirect(url_for('Mon_compte'))

@app.route('/modifier_mdp', methods=['POST'])
def modifier_mdp():
    if 'logged_in' not in session:
        return redirect(url_for('Connexion'))
        
    ancien_mdp = request.form['ancien_mdp']
    nouveau_mdp = request.form['nouveau_mdp']
    conf_mdp = request.form['conf_nouveau_mdp']
    username = session['username']

    if nouveau_mdp != conf_mdp:
        # Idéalement, utiliser 'flash' pour afficher l'erreur
        print("Les mots de passe ne correspondent pas")
        return redirect(url_for('Mon_compte'))

    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    # Vérifier l'ancien mot de passe
    c.execute("SELECT mdp_haché FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?", (username,))
    result = c.fetchone()
    
    if result and check_password_hash(result[0], ancien_mdp):
        # Hacher le nouveau mot de passe
        nouveau_hash = generate_password_hash(nouveau_mdp)
        c.execute("UPDATE Utilisateur_Intervenant SET mdp_haché = ? WHERE nom_utilisateur = ?", (nouveau_hash, username))
        db.commit()
        print("Mot de passe modifié avec succès")
    else:
        print("Ancien mot de passe incorrect")
        
    db.close()
    return redirect(url_for('Mon_compte'))

# --- Routes Publiques (Laissées sans Gardien) ---

@app.route('/Connexion')
def Connexion():
    titre_site = "Site interne TNS"
    # Cette page doit être accessible à tous
    return render_template('Connexion.html', titre=titre_site, titre_page_actuelle="Connexion")

# ... (votre fonction login() sécurisée que nous avons construite va ici) ...
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 1. Vérifier si l'utilisateur a soumis le formulaire (POST)
    if request.method == 'POST':
        # 2. Récupérer les données du formulaire
        username = request.form['identifiant']
        password = request.form['mot_de_passe']
        
        db = sqlite3.connect(DATABASE)
        c = db.cursor()
        sql = "SELECT idi, mdp_haché, pdp_url, fonction, status FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?"
        c.execute(sql, (username,))
        result = c.fetchone()
        db.close()
        if result:
            id_recupere=result[0]
            mdp_hash = result[1]
            pdp_url = result[2]
            fonction = result[3]
            status = result[4]
        else:
            id_recupere=None
            mdp_hash = None
            pdp_url = None
            fonction=None
            status=None
        
        if mdp_hash and check_password_hash(mdp_hash, password):
            if status == 0:
                erreur = "Compte inactif. Contactez l'administrateur."
                return render_template('Connexion.html', erreur=erreur)
            # Succès ! Stocker les informations
            session['logged_in'] = True
            session['username'] = username
            session['user_id']=id_recupere
            session['pdp_url'] = pdp_url # On stocke l'URL dans la session !
            session['fonction'] = fonction if fonction else 'user' # Rôle par défaut 'user'
            return redirect(url_for('Accueil'))
        else:
            # 4. Si les informations sont incorrectes, afficher un message d'erreur
            erreur = "Identifiant ou mot de passe incorrect."
            return render_template('Connexion.html', erreur=erreur)
    # 3. Si c'est une requête GET, ou après une tentative non concluante, afficher le formulaire
    return render_template('Connexion.html')

# ... (votre fonction logout() ci-dessus va ici) ...
@app.route('/logout')
def logout():
    session.clear() # ⬅️ Efface toutes les clés de la session
    return redirect(url_for('Connexion')) # Redirige vers la page de connexion


@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    file = request.files.get('pdp_file')

    # Vérification unique et complète (existence + sécurité de l'extension)
    if file and file.filename != '' and allowed_file(file.filename):
        try:
            # 1. Préparation du nom sécurisé (ex: admin.jpg)
            extension = file.filename.rsplit('.', 1)[1].lower()
            username = session['username']
            secure_filename = f"{username}.{extension}"
            
            # 2. Sauvegarde du fichier sur le disque
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename)
            file.save(full_path)
            
            # 3. Mise à jour de la BDD
            url_to_save = os.path.join('images/profiles', secure_filename) # Chemin relatif pour la BDD/HTML
            
            db = sqlite3.connect(DATABASE)
            c = db.cursor()
            sql_update = "UPDATE Utilisateur_Intervenant SET pdp_url = ? WHERE nom_utilisateur = ?"
            c.execute(sql_update, (url_to_save, username))
            
            db.commit()
            session['pdp_url'] = url_to_save
            db.close()

            # Succès : Retour à la page de profil
            return redirect(url_for('Mon_compte'))

        except Exception as e:
            # Gérer les erreurs (problème de BDD ou de disque)
            print(f"Erreur lors de l'upload ou de la mise à jour : {e}")
            # Idéalement, utilisez un message flash ici
            return redirect(url_for('Mon_compte'))
            
    else:
        # Échec de la vérification (pas de fichier soumis ou extension non autorisée)
        return redirect(url_for('Mon_compte'))

# --- ROUTE : TÉLÉCHARGER SES DONNÉES (Export JSON) ---
@app.route('/telecharger_donnees')
def telecharger_donnees():
    if 'logged_in' not in session:
        return redirect(url_for('Connexion'))
    
    username = session['username']
    
    try:
        db = sqlite3.connect(DATABASE)
        # On configure la connexion pour récupérer les résultats sous forme de dictionnaire (plus facile pour le JSON)
        db.row_factory = sqlite3.Row 
        c = db.cursor()
        
        # 1. Récupération des infos utilisateur
        sql = "SELECT UI.nom_utilisateur, UI.email_utilisateur, UI.pdp_url, I.role, I.prenom, I.nom, PC.niveau, C.competence FROM Utilisateur_Intervenant UI LEFT JOIN Intervenants I ON UI.idi = I.idi LEFT JOIN PossedeCompetence PC ON I.idi = PC.idi LEFT JOIN Competences C ON PC.idcomp = C.idcomp WHERE nom_utilisateur = ?"
        c.execute(sql, (username,))
        rows = c.fetchall()
        
        db.close()

        if rows:
            first_row = rows[0]
            # Agrégation des compétences
            liste_competences = []
            for row in rows:
                if row['competence']:
                    liste_competences.append({
                        "competence": row['competence'],
                        "niveau": row['niveau']
                    })
            # 2. Création du dictionnaire de données
            donnees = {
                "profil": {
                    "nom_utilisateur": first_row['nom_utilisateur'],
                    "email": first_row['email_utilisateur'],
                    "photo_profil": first_row['pdp_url'],
                    "role": first_row['role'],
                    "prenom": first_row['prenom'],
                    "nom": first_row['nom'],
                    "competences": liste_competences
                    
                },
                "statut": "Actif",
                "date_export": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 3. Conversion en JSON
            json_str = json.dumps(donnees, indent=4, ensure_ascii=False)
            
            # 4. Création de la réponse "Fichier à télécharger"
            return Response(
                json_str,
                mimetype="application/json",
                headers={"Content-Disposition": f"attachment;filename=donnees_{username}.json"}
            )
        else:
            return "Erreur : Données introuvables", 404

    except Exception as e:
        return f"Erreur lors de l'export : {e}"


# --- ROUTE : SUPPRIMER LE COMPTE ---
@app.route('/supprimer_compte')
def supprimer_compte():
    if 'logged_in' not in session:
        return redirect(url_for('Connexion'))
    
    username = session['username']
    
    try:
        db = get_db()
        cursor = db.cursor()
        
        # ÉTAPE 1 : On récupère l'ID de l'intervenant (idi) avant de supprimer le compte
        # Cela nous servira à supprimer aussi son profil "Physique" (Nom, Prénom)
        cursor.execute("SELECT idi FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?", (username,))
        result = cursor.fetchone()
        
        idi_a_supprimer = result['idi'] if result else None
        
        # ÉTAPE 2 : Supprimer le compte de connexion (Utilisateur_Intervenant)
        cursor.execute("DELETE FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?", (username,))
        
        # ÉTAPE 3 : Supprimer la fiche intervenant 
        if idi_a_supprimer:
            cursor.execute("DELETE FROM Intervenants WHERE idi = ?", (idi_a_supprimer,))

        # ÉTAPE 4 : Supprimer la fiche PC 
        if idi_a_supprimer:
            cursor.execute("DELETE FROM PossedeCompetence WHERE idi = ?", (idi_a_supprimer,)) 

        # ÉTAPE 5 : Valider les changements
        db.commit()
        
        # Déconnexion et retour à l'accueil
        session.clear()
        flash("Votre compte a été supprimé définitivement.", "success")
        return redirect(url_for('Connexion'))
        
    except Exception as e:
        db.rollback()
        flash(f"Erreur lors de la suppression : {e}", "error")
        return redirect(url_for('Mon_compte'))




def normalize_text(text):
    if not text:
        return ""
    # on enlève toutes les majuscules
    text = text.lower()
    # on passe en NFD puis suppression des marques ( é = e + accent)
    normalized = unicodedata.normalize('NFD', text)
    
    # On filtre pour ne garder que le caractère de base
    text_sans_accents = "".join(char for char in normalized if unicodedata.category(char) != 'Mn')
    return text_sans_accents


    
@app.route('/Intervenants/<nomcomplet>')
def Inter_profil(nomcomplet=None):
    # 1. Sécurité sur le format de l'URL
    try:
        [name, surname] = nomcomplet.split('.')
    except ValueError:
        return "Format URL invalide (attendu: Nom.Prenom)", 400

    db = get_db()
    c = db.cursor()
    
    # 2. On prépare les noms pour la recherche
    name_search = name
    surname_search = surname

    # 3. LA REQUÊTE SQL AVEC ALIAS ET LEFT JOIN
    # I  = Intervenants
    # PC = PossedeCompetence
    # C  = Competences
    sql = """
    SELECT
        I.idi,
        I.nom, 
        I.prenom,
        I.dispo,
        I.role,
        UI.pdp_url,
        UI.nom_utilisateur,
        UI.email_utilisateur,
        C.competence, 
        PC.niveau
    FROM Intervenants I
    LEFT JOIN PossedeCompetence PC ON I.idi = PC.idi
    LEFT JOIN Competences C ON C.idcomp = PC.idcomp
    LEFT JOIN Utilisateur_Intervenant UI ON I.idi = UI.idi
    WHERE I.nom = ? AND I.prenom = ?
    """
    
    c.execute(sql, (name_search, surname_search))
    rows = c.fetchall()

    # 4. Vérification : Si la liste est vide, c'est que la personne n'existe vraiment pas
    if not rows:
       return render_template("error_intervenant.html", message="Intervenant non trouvé")

    # 5. On récupère les infos de base (sur la première ligne)
    id_intervenant = rows[0]['idi']
    nom_affiche = normalize_text(rows[0]['nom'])
    prenom_affiche = normalize_text(rows[0]['prenom'])
    dispo = rows[0]['dispo']
    pdp_actuelle = rows[0]['pdp_url']
    nom_utilisateur = rows[0]['nom_utilisateur']
    email_utilisateur = rows[0]['email_utilisateur']
    role = rows[0]['role']
    
    # 6. On boucle pour récupérer les compétences (si elles existent)
    competences = []
    for row in rows:
        # Grâce au LEFT JOIN, 'competence' sera None si l'admin n'en a pas.
        # On ne l'ajoute à la liste que si ce n'est pas None.
        if row["competence"]: 
            competences.append({
                "nom": row["competence"],
                "niveau": row["niveau"]
            })

    return render_template('Intervenant_profil.html',
                           id_intervenant=id_intervenant,
                           nom=nom_affiche, 
                           prenom=prenom_affiche, 
                           competences=competences,
                           dispo=dispo,
                           pdp_actuelle=pdp_actuelle,
                           nom_utilisateur=nom_utilisateur,
                           email_utilisateur=email_utilisateur,
                           titre_page_actuelle="Profil Intervenant",
                           role=role
                           )


@app.route('/Clients/<nomcomplet>')
def Client_profil(nomcomplet=None):
    # 1. Sécurité sur le format de l'URL
    try:
        [name, surname] = nomcomplet.split('.')
    except ValueError:
        return "Format URL invalide (attendu: Nom.Prenom)", 400

    db = get_db()
    c = db.cursor()
    
    # 2. On prépare les noms pour la recherche
    name_search = normalize_text(name) 
    surname_search = normalize_text(surname)

    # 3. LA REQUÊTE SQL AVEC ALIAS ET LEFT JOIN
    # C  = Clients
    # P = Projets
    sql = """
    SELECT 
        C.idc,
        C.nom, 
        C.prenom, 
        C.secteur, 
        C.telephone,
        C.email,
        C.dernier_contact,
        P.idp,
        P.etat

    FROM Clients C
    LEFT JOIN Projets P ON C.idc = P.idc
    WHERE C.nom = ? AND C.prenom = ?
    """
    
    c.execute(sql, (name_search, surname_search))
    rows = c.fetchall()

    # 4. Vérification : Si la liste est vide, c'est que la personne n'existe vraiment pas
    if not rows:
       return render_template("error_client.html", message="Nous n'avons pas encore travaillé avec cette personne, vérifiez peut-être l'orthographe ")

    # 5. On récupère les infos de base (sur la première ligne)
    id_clients = rows[0]['idc']
    nom_affiche = rows[0]['nom']
    prenom_affiche = rows[0]['prenom']
    secteur=rows[0]['secteur']
    telephone=rows[0]['telephone']
    dernier_contact=rows[0]['dernier_contact']
    email=rows[0]['email']

    
    # 6. On boucle pour récupérer les compétences (si elles existent)
    projets = []
    for row in rows:
        # Grâce au LEFT JOIN, 'competence' sera None si l'admin n'en a pas.
        # On ne l'ajoute à la liste que si ce n'est pas None.
        if row["idp"]: 
            projets.append({
                "idp": row["idp"],
                "etat": row["etat"]
            })


    sql1="""
    SELECT IC.date_interaction, IC.type_interaction, IC.contenu, IC.idp, P.etat
    FROM InteractionClient IC
    LEFT JOIN Clients C ON C.idc = IC.idc
    LEFT JOIN Projets P ON P.idp = IC.idp
    WHERE C.nom = ? AND C.prenom = ?
    ORDER BY IC.idp, IC.date_interaction DESC
    """
    c.execute(sql1, (name_search, surname_search))
    rows = c.fetchall()

    interactions = {}
    interactions_done = {}


    for row in rows:
        date_interaction, type_interaction, contenu, idp, etat = row
        if etat=='Terminé':
            if idp not in interactions_done:
                interactions_done[idp] = []
            
            interactions_done[idp].append({
                'date': date_interaction,
                'type': type_interaction,
                'contenu': contenu,
                'etat': etat  })
        else:
            if idp not in interactions:
                interactions[idp] = []
            
            interactions[idp].append({
                'date': date_interaction,
                'type': type_interaction,
                'contenu': contenu,
                'etat': etat })

    return render_template('Client_profil.html',
                           id_clients = id_clients,
                           nom=nom_affiche, 
                           prenom=prenom_affiche, 
                           secteur=secteur,
                           telephone=telephone,
                           dernier_contact=dernier_contact,
                           email=email,
                           projets=projets,
                           titre_page_actuelle="Profil Client",
                           interactions = interactions, interactions_done=interactions_done
                           )


@app.route('/Inscription', methods=['GET', 'POST'])
def Inscription():
    if request.method == 'POST':
        # Récupération sécurisée des données
        username = request.form.get('nom_utilisateur')
        email = request.form.get('email')
        password = request.form.get('mot_de_passe')
        confirm_password = request.form.get('confirmation_mdp')
        prenom = request.form.get('prenom')
        nom = request.form.get('nom')
        liste_competences = request.form.getlist('competence[]')
        liste_niveaux = request.form.getlist('niveau[]')

        # --- Vérification 1 : Champs non vides ---
        if not all([username, email, password, confirm_password, prenom, nom]):
            erreur = "Veuillez remplir tous les champs obligatoires."
            return render_template('Inscription.html', erreur=erreur)

        # --- Vérification 2 : Mots de passe correspondants ---
        if password != confirm_password:
            erreur = "Les mots de passe ne correspondent pas."
            return render_template('Inscription.html', erreur=erreur)

        # Si nous arrivons ici, les données sont complètes et les mots de passe correspondent.
        
        # 3. Vérification de l'existence de l'utilisateur (Prochaine étape !)
        db = get_db()
        c = db.cursor()
        
        sql_check = "SELECT COUNT(*) FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?"
        c.execute(sql_check, (username,))
        
        # Récupère le compte (le résultat est un tuple, ex: (1,))
        count = c.fetchone()[0]
        
        if count > 0:
            # L'utilisateur existe déjà !
            erreur = f"Le nom d'utilisateur '{username}' est déjà pris."
            return render_template('Inscription.html', erreur=erreur)

        # Si nous arrivons ici, le nom d'utilisateur est unique.
        
        # 4. Hachage du mot de passe avant stockage
        hashed_password = generate_password_hash(password)

        # 5. Insertion dans la BDD
        try:
            db = get_db()
            cursor = db.cursor()
            
            # --- 5A. Insertion dans Intervenants (Profil Personnel) ---
            # Récupérer l'idi généré
            date_inscription = datetime.now().strftime('%d/%m/%Y')
            sql_intervenant = """
                INSERT INTO Intervenants (nom, prenom, date_inscription) 
                VALUES (?, ?, ?)
            """
            cursor.execute(sql_intervenant, (nom, prenom, date_inscription))
            idi = cursor.lastrowid

            for competence_nom, niveau_val in zip(liste_competences, liste_niveaux):
            
                # Nettoyage des données (enlever les espaces inutiles)
                competence_clean = competence_nom.strip()
                
                # Sécurité : On ignore les lignes vides (si l'utilisateur a cliqué sur + sans remplir)
                if not competence_clean:
                    continue 

                # --- 5B. Insertion dans Competences (LOGIQUE INTÉGRÉE DANS LA BOUCLE) ---
                
                # On vérifie si la compétence existe déjà
                sql_check_comp = "SELECT idcomp FROM Competences WHERE competence = ?"
                cursor.execute(sql_check_comp, (competence_clean,))
                comp_result = cursor.fetchone()

                if comp_result:
                    idcomp = comp_result[0]
                else:
                    # Si elle n'existe pas, on l'insère
                    sql_comp = "INSERT INTO Competences (competence) VALUES (?)"
                    cursor.execute(sql_comp, (competence_clean,))
                    idcomp = cursor.lastrowid
                
                # --- 5C. Insertion dans PossedeCompetence (Lien) ---
                
                sql_possede = """
                    INSERT INTO PossedeCompetence (idi, idcomp, niveau) 
                    VALUES (?, ?, ?)
                """

                cursor.execute(sql_possede, (idi, idcomp, niveau_val))

            # --- 5D. Insertion dans Utilisateur_Intervenant (Compte de Connexion) ---
            
            sql_utilisateur = """
                INSERT INTO Utilisateur_Intervenant 
                (mdp_haché, idi, nom_utilisateur, pdp_url, email_utilisateur, fonction, status) 
                VALUES (?, ?, ?, ?, ?, 'user', 0)
            """
            # Valeurs par défaut : pdp_url est vide au départ
            pdp_default = ''
            cursor.execute(sql_utilisateur, (hashed_password, idi, username, pdp_default, email))

            db.commit() 

        except sqlite3.Error as e:
            # En cas d'erreur de BDD, on annule tout
            erreur = f"Erreur de base de données lors de l'inscription : {e}"
            return render_template('Inscription.html', erreur=erreur)

        # 6. Redirection après succès
        # Après une inscription réussie, redirigez l'utilisateur vers la page de connexion
        return redirect(url_for('Connexion'))
        
    # Si la méthode est GET, on affiche le formulaire
    return render_template('Inscription.html', titre_page_actuelle="Inscription")


@app.route('/export_client', methods=['POST'])
def export_client():
    # 1. On récupère l'ID directement depuis le formulaire
    client_id = request.form.get('client_id')

    # Sécurité : Si aucun ID n'est envoyé, on recharge la page
    if not client_id:
        return redirect(url_for('Import_Export'))

    # 2. Connexion BDD
    db = get_db()
    cursor = db.cursor()
    
    # 3. Requête SQL
    sql = "SELECT * FROM Clients WHERE idc = ?"
    cursor.execute(sql, (client_id,)) 
    client_data = cursor.fetchone() 
    
    # Si le client n'existe pas
    if not client_data:
        return "Erreur : Client non trouvé.", 404

    # 4. Mise en forme CSV (Identique à avant)
    headers = client_data.keys()
    values = list(client_data) 
    
    csv_headers = ','.join(headers)
    csv_data = ','.join([str(v) for v in values])
    csv_content = f"{csv_headers}\n{csv_data}"

    # 5. Envoi direct du fichier
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=client_{client_id}.csv"}
    )

@app.route('/import_clients', methods=['POST'])
def import_clients():
    # 1. Vérification que le fichier est présent
    if 'csv_file' not in request.files:
        return redirect(url_for('Import_Export'))
    
    file = request.files['csv_file']
    
    # 2. Vérification que le nom de fichier n'est pas vide
    if file.filename == '':
        return redirect(url_for('Import_Export'))

    if file:
        # 3. Transformation du fichier binaire en fichier texte pour le module CSV
        # On utilise io.TextIOWrapper pour décoder les bytes en string (UTF-8)
        stream = io.TextIOWrapper(file.stream._file, "utf8", newline=None)
        
        # 4. Lecture du CSV en mode "Dictionnaire"
        # Cela permet d'appeler les colonnes par leur nom (ex: row['nom']) peu importe l'ordre
        csv_input = csv.DictReader(stream)
        
        db = get_db()
        cursor = db.cursor()
        
        try:
            nb_ajouts = 0
            nb_doublons = 0

            # On prépare la requête d'insertion (AVEC l'idc cette fois)
            # Puisqu'on vérifie l'ID, on doit aussi l'insérer pour garder la cohérence
            sql_insert = """
                INSERT INTO Clients (idc, nom, prenom, email, telephone, secteur, dernier_contact, nom_entreprise) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """

            for row in csv_input:
                # 1. On récupère l'IDC du fichier CSV
                id_client = row['idc']
                
                # 2. VÉRIFICATION : Est-ce que cet IDC existe déjà dans la base ?
                sql_verif = "SELECT idc FROM Clients WHERE idc = ?"
                cursor.execute(sql_verif, (id_client,))
                existe = cursor.fetchone()

                if existe:
                    # 3. CAS DOUBLON : L'ID existe déjà, on ignore cette ligne
                    nb_doublons += 1
                    continue 
                
                # 4. CAS NOUVEAU : On insère la ligne (en forçant l'IDC du fichier)
                cursor.execute(sql_insert, (
                    row['idc'],  # On insère l'ID du fichier
                    row['nom'], 
                    row['prenom'], 
                    row['email'], 
                    row['telephone'], 
                    row['secteur'], 
                    row['dernier_contact'], 
                    row['nom_entreprise']
                ))
                nb_ajouts += 1
            
            db.commit()

            if nb_ajouts > 0:
                flash(f"Succès ! {nb_ajouts} clients importés ({nb_doublons} ID existants ignorés).", "success")
            elif nb_doublons > 0:
                flash(f"Aucun import : les {nb_doublons} clients du fichier existent déjà (basé sur l'IDC).", "error")
            else:
                flash("Le fichier semblait vide ou incorrect.", "error")

            return redirect(url_for('Import_Export'))
            
        except Exception as e:
            db.rollback()
            flash(f"Erreur technique : {e}", "error")
            return redirect(url_for('Import_Export'))

    return redirect(url_for('Import_Export'))

@app.route('/supprimer_client/<int:id_clients>', methods=['POST'])
def supprimer_client(id_clients):
    if 'logged_in' not in session:
        return redirect(url_for('Connexion'))
    
    if session.get('fonction') != 'admin':
        flash("Action non autorisée. Vous devez être administrateur.", "error")
        return redirect(url_for('Clients'))
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("DELETE FROM Projets WHERE idc = ?", (id_clients,))
        cursor.execute("DELETE FROM Historique WHERE idc = ?", (id_clients,))
        cursor.execute("DELETE FROM Clients WHERE idc = ?", (id_clients,))
        
        # Valider les changements
        db.commit()
        flash("Le compte client a été supprimé définitivement.", "success")
        return redirect(url_for('Clients'))
        
    except Exception as e:
        db.rollback()
        print(f"Erreur SQL : {e}")
        return f"Erreur lors de la suppression du client : {e}"
    
@app.route('/upload_client/<int:id_clients>', methods=['POST'])
def upload_client(id_clients):
    if 'logged_in' not in session:
        return redirect(url_for('Connexion'))
    
    if session.get('fonction') != 'admin':
        flash("Action non autorisée. Vous devez être administrateur.", "error")
        return redirect(url_for('Clients'))
    
    db = get_db()
    c = db.cursor()
    
    try:
        # 1. Récupération des infos utilisateur
        sql = "SELECT C.nom, C.prenom, C.email, C.telephone, C.secteur, C.dernier_contact, C.nom_entreprise, H.date, H.interaction_text, P.etat, P.budget, P.deb, P.fin, P.titre_projet FROM Clients C LEFT JOIN Projets P ON P.idc = C.idc LEFT JOIN Historique H ON H.idc = C.idc WHERE C.idc = ?"
        c.execute(sql, (id_clients,))
        rows = c.fetchall()
        
        db.close()

        if rows:
            first_row = rows[0]
            # Agrégation des compétences
            liste_historique = []
            for row in rows:
                if row['date']:
                    liste_historique.append({
                        "date": row['date'],
                        "interaction_text": row['interaction_text']
                    })
            liste_projets = []
            for row in rows:
                if row['date']:
                    liste_projets.append({
                        "titre_projet": row['titre_projet'],
                        "etat": row['etat'],
                        "budget": row['budget'],
                        "deb": row['deb'],
                        "fin": row['fin'],
                    })
            # 2. Création du dictionnaire de données
            donnees = {
                "profil_client": {
                    "nom": first_row['nom'],
                    "prenom": first_row['prenom'],
                    "email": first_row['email'],
                    "telephone": first_row['telephone'],
                    "secteur": first_row['secteur'],
                    "dernier_contact": first_row['dernier_contact'],
                    "nom_entreprise": first_row['nom_entreprise'],
                    "historique": liste_historique,
                    "projets" : liste_projets
                    
                },
                "statut": "Actif",
                "date_export": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 3. Conversion en JSON
            json_str = json.dumps(donnees, indent=4, ensure_ascii=False)
            
            # 4. Création de la réponse "Fichier à télécharger"
            return Response(
                json_str,
                mimetype="application/json",
                headers={"Content-Disposition": f"attachment;filename=donnees_{id_clients}.json"}
            )
        else:
            return "Erreur : Données introuvables", 404

    except Exception as e:
        return f"Erreur lors de l'export : {e}"
    
@app.route('/supprimer_intervenant/<int:id_intervenant>', methods=['POST'])
def supprimer_intervenant(id_intervenant):
    if 'logged_in' not in session:
        return redirect(url_for('Connexion'))
    
    if session.get('fonction') != 'admin':
        flash("Action non autorisée. Vous devez être administrateur.", "error")
        return redirect(url_for('Intervenants'))
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        # --- ÉTAPE 1 : VÉRIFICATION (Est-ce mon propre compte ?) ---
        # On regarde à quel nom d'utilisateur appartient cet ID intervenant
        sql_check = "SELECT nom_utilisateur FROM Utilisateur_Intervenant WHERE idi = ?"
        cursor.execute(sql_check, (id_intervenant,))
        result = cursor.fetchone()
        
        # On prépare un "drapeau" (flag) pour savoir si on devra déconnecter à la fin
        c_est_mon_compte = False
        if result:
            # Si le nom d'utilisateur lié à cet ID est le même que celui dans la session actuelle
            if result['nom_utilisateur'] == session.get('username'):
                c_est_mon_compte = True

        cursor.execute("DELETE FROM Utilisateur_Intervenant WHERE idi = ?", (id_intervenant,))
        cursor.execute("DELETE FROM PossedeCompetence WHERE idi = ?", (id_intervenant,))
        cursor.execute("DELETE FROM Participation WHERE idi = ?", (id_intervenant,))
        cursor.execute("DELETE FROM Historique WHERE idi = ?", (id_intervenant,))
        cursor.execute("DELETE FROM Documents WHERE idi = ?", (id_intervenant,))
        cursor.execute("DELETE FROM Intervenants WHERE idi = ?", (id_intervenant,))

        db.commit()
        
        # --- ÉTAPE 3 : LOGIQUE DE REDIRECTION ---
        if c_est_mon_compte:
            # Si j'ai supprimé mon propre compte, je vide la session et je vais au login
            session.clear()
            flash("Votre compte a été supprimé avec succès. Au revoir !", "info")
            return redirect(url_for('Connexion')) # Assurez-vous que la route s'appelle bien 'Connexion' ou 'login'
        else:
            # Si c'est un admin qui supprime un autre collègue, on reste sur la liste
            flash("Le compte intervenant a été supprimé définitivement.", "success")
            return redirect(url_for('Intervenants')) # Ou 'Accueil' selon votre préférence
        
    except Exception as e:
        db.rollback()
        print(f"Erreur SQL : {e}")
        flash(f"Erreur lors de la suppression : {e}", "error")
        return redirect(url_for('Intervenants')) # Redirection de sécurité en cas d'erreur  
    
@app.route('/upload_intervenant/<int:id_intervenant>', methods=['POST'])
def upload_intervenant(id_intervenant):
    if 'logged_in' not in session:
        return redirect(url_for('Connexion'))
    
    if session.get('fonction') != 'admin':
        flash("Action non autorisée. Vous devez être administrateur.", "error")
        return redirect(url_for('Intervenants'))
    
    db = get_db()
    c = db.cursor()
    
    try:
        # 1. Récupération des infos utilisateur
        sql = "SELECT UI.nom_utilisateur, UI.email_utilisateur, UI.pdp_url, I.role, I.prenom, I.nom, PC.niveau, C.competence FROM Utilisateur_Intervenant UI LEFT JOIN Intervenants I ON UI.idi = I.idi LEFT JOIN PossedeCompetence PC ON I.idi = PC.idi LEFT JOIN Competences C ON PC.idcomp = C.idcomp WHERE I.idi = ?"
        c.execute(sql, (id_intervenant,))
        rows = c.fetchall()
        
        db.close()

        if rows:
            first_row = rows[0]
            # Agrégation des compétences
            liste_competences = []
            for row in rows:
                if row['competence']:
                    liste_competences.append({
                        "competence": row['competence'],
                        "niveau": row['niveau']
                    })
            # 2. Création du dictionnaire de données
            donnees = {
                "profil": {
                    "nom_utilisateur": first_row['nom_utilisateur'],
                    "email": first_row['email_utilisateur'],
                    "photo_profil": first_row['pdp_url'],
                    "role": first_row['role'],
                    "prenom": first_row['prenom'],
                    "nom": first_row['nom'],
                    "competences": liste_competences
                    
                },
                "statut": "Actif",
                "date_export": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 3. Conversion en JSON
            json_str = json.dumps(donnees, indent=4, ensure_ascii=False)
            
            # 4. Création de la réponse "Fichier à télécharger"
            return Response(
                json_str,
                mimetype="application/json",
                headers={"Content-Disposition": f"attachment;filename=donnees_{id_intervenant}.json"}
            )
        else:
            return "Erreur : Données introuvables", 404

    except Exception as e:
        return f"Erreur lors de l'export : {e}"



@app.route('/api/recherche/clients', methods=['GET'])
def recherche_secteur_client():
    """
    Récupère le secteur depuis l'URL et renvoie les liens de profil correspondants.
    """
    secteur = request.args.get('secteur', default='', type=str).strip()
    
    if not secteur:
        return jsonify({"profils": [], "message": "Le paramètre 'secteur' est manquant."}), 400


    profils = []
    
    try:
        db = get_db()
        c = db.cursor()
        
        # 1. Préparation de la valeur de recherche pour la fonction LIKE
    
        search_secteur = f"%{secteur}%"

        # 2. La Requête SQL avec le Placeholder Sécurisé (?)
        # La requête est sécurisée contre l'injection SQL
        sql = """
        SELECT
            nom, prenom
        FROM
            Clients
        WHERE
            secteur LIKE ?; 
        """
        
        # 3. Exécution de la Requête PRÉPARÉE
        c.execute(sql, (search_secteur,)) 
        
        results = c.fetchall()
        for row in results:
                    prenom = row['prenom'].lower()
                    nom = row['nom'].lower()
                    lien_profil = f"/Clients/{nom}.{prenom}"   
                    profils.append(lien_profil) 
                  
        
     
    except sqlite3.Error as e:
            print(f"Erreur de base de données SQLite : {e}")
            return jsonify({"profils": [], "error": "Erreur serveur lors de l'accès à la base de données."}), 500  
   

    return jsonify({
        "profils": profils,
        "count": len(profils),
    })

@app.route('/export_mission/<int:id_projet>', methods=['POST'])
def export_mission(id_projet):
    # 1. On récupère l'ID des projets finis
    db = get_db()
    cursor = db.cursor()
    try:
        sql = """
        SELECT 
            P.titre_projet, 
            P.deb, 
            P.fin, 
            P.budget, 
            P.etat, 
            C.nom AS nom_client, 
            C.prenom AS prenom_client, 
            C.nom_entreprise, 
            I.nom AS nom_intervenant, 
            I.prenom AS prenom_intervenant 
        FROM Projets P 
        LEFT JOIN Clients C ON P.idc = C.idc 
        LEFT JOIN Participation PA ON P.idp = PA.idp 
        LEFT JOIN Intervenants I on PA.idi = I.idi 
        WHERE P.idp = ?
        """
       
        cursor.execute(sql, (id_projet,))
        projets_data = cursor.fetchall()
        
        # 2. Mise en forme CSV
        if not projets_data:
            return redirect(url_for('Missions_réalisées'))
        
        # Préparer les en-têtes
        headers = projets_data[0].keys()
        csv_headers = ','.join(headers)
        
        # Préparer les lignes de données
        csv_lines = []
        for projet in projets_data:
            values = [str(projet[h]) for h in headers]
            csv_lines.append(','.join(values))
        
        csv_content = f"{csv_headers}\n" + "\n".join(csv_lines)
        
        # 3. Envoi direct du fichier
        return Response(
            csv_content,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=projets_termines.csv"}
        )    
    except Exception as e:
        return f"Erreur lors de l'export : {e}"

@app.route('/admin/utilisateurs_en_attente')
def admin_validation():
    # On récupère le nom de l'utilisateur connecté
    username = session.get('username')
    if not username:
        return redirect(url_for('Connexion')) # Si pas connecté, on renvoie au login
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT fonction FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?", (username,))
    user_info = cursor.fetchone()

    if not user_info or user_info['fonction'] != 'admin':
        return redirect(url_for('Accueil'))
    
    cursor.execute("SELECT * FROM Utilisateur_Intervenant WHERE status = 0")
    utilisateurs_en_attente = cursor.fetchall()
    
    return render_template('admin_validation.html', utilisateurs=utilisateurs_en_attente)

@app.route('/admin/valider/<int:id>', methods=['POST'])
def valider_utilisateur(id):
    if session.get('fonction') != 'admin':
        return redirect(url_for('Connexion'))
        
    db = get_db()
    db.execute("UPDATE Utilisateur_Intervenant SET status = 1 WHERE idu = ?", (id,))
    db.commit()
    
    flash("Utilisateur validé avec succès.", "success")
    return redirect(url_for('admin_validation'))

@app.route('/admin/refuser/<int:id>', methods=['POST'])
def refuser_utilisateur(id):
    if session.get('fonction') != 'admin':
        return redirect(url_for('Connexion'))
        
    db = get_db()
    # Si on refuse, on supprime carrément la demande d'inscription
    # On doit aussi supprimer l'intervenant lié
    cursor = db.cursor()
    cursor.execute("SELECT idi FROM Utilisateur_Intervenant WHERE idu = ?", (id,))
    result = cursor.fetchone()
    id_intervenant = result['idi'] if result else None
    if id_intervenant:
        db.execute("DELETE FROM PossedeCompetence WHERE idi = ?", (id_intervenant,))
        db.execute("DELETE FROM Intervenants WHERE idi = ?", (id_intervenant,))
    db.execute("DELETE FROM Utilisateur_Intervenant WHERE idu = ?", (id,))    
    db.commit()
    
    flash("Inscription refusée et supprimée.", "warning")
    return redirect(url_for('admin_validation'))

@app.route('/admin/definir_role/<int:id_intervenant>', methods=['POST'])
def definir_role(id_intervenant):
    # 1. SÉCURITÉ : Seul l'admin peut faire ça
    if session.get('fonction') != 'admin':
        flash("Action non autorisée.", "error")
        return redirect(url_for('profil_intervenant', id=id_intervenant))
    
    # 2. Récupération du nouveau rôle depuis le formulaire
    nouveau_role = request.form.get('role_metier')
    
    db = get_db()
    cursor = db.cursor()
    try:
        # On met à jour la colonne 'role' de la table Intervenants
        db.execute("UPDATE Intervenants SET role = ? WHERE idi = ?", (nouveau_role, id_intervenant))
        db.commit()
        flash(f"Le rôle a été modifié en : {nouveau_role}", "success")
        cursor.execute("SELECT nom, prenom FROM Intervenants WHERE idi = ?", (id_intervenant,))
        row = cursor.fetchone()
        
        if row:
            # On reconstruit le format "Nom.Prenom" attendu par ta route
            nom_complet_url = f"{row['nom']}.{row['prenom']}"
            return redirect(url_for('Inter_profil', nomcomplet=nom_complet_url))
        
    except Exception as e:
        flash(f"Erreur lors de la mise à jour : {e}", "error")
    return redirect(url_for('Accueil'))

import json

@app.route('/carte_clients')
def carte_clients():
    if 'logged_in' not in session:
        return redirect(url_for('Connexion'))
    
    db = get_db()
    cursor = db.cursor()
    
    # On récupère uniquement les clients qui ont une latitude et une longitude définies
    sql = """
    SELECT nom, prenom, nom_entreprise, adresse, lattitude, longitude 
    FROM Clients 
    WHERE lattitude IS NOT NULL AND longitude IS NOT NULL
    """
    cursor.execute(sql)
    clients_data = cursor.fetchall()
    
    clients_list = []
    for client in clients_data:
        clients_list.append({
            "nom": f"{client['nom']} {client['prenom']}",
            "entreprise": client['nom_entreprise'],
            "adresse": client['adresse'],
            "lat": client['lattitude'],
            "lon": client['longitude']
        })
    
    return render_template('carte_clients.html', clients=clients_list)

@app.route('/ajouter_client', methods=['GET', 'POST'])
def ajouter_client():
    # 1. SÉCURITÉ : On vérifie si c'est un admin
    if session.get('fonction') != 'admin':
        flash("Accès refusé. Vous devez être administrateur.", "error")
        return redirect(url_for('Clients')) # Ou Accueil

    if request.method == 'POST':
        # 2. Récupération des données du formulaire
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        entreprise = request.form.get('entreprise')
        secteur = request.form.get('secteur')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        adresse = request.form.get('adresse')
        
        # 3. GÉOCODAGE AUTOMATIQUE (Pour la carte)
        # On utilise la fonction qu'on a créée précédemment
        lat, lon = None, None
        if adresse:
            lat, lon = geocode_adresse(adresse)
        
        # 4. Enregistrement en Base de Données
        try:
            db = get_db()
            sql = """
                INSERT INTO Clients (nom, prenom, nom_entreprise, secteur, email, telephone, adresse, lattitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.execute(sql, (nom, prenom, entreprise, secteur, email, telephone, adresse, lat, lon))
            db.commit()
            
            flash(f"Le client {entreprise} a été ajouté avec succès !", "success")
            return redirect(url_for('Clients'))
            
        except Exception as e:
            flash(f"Erreur lors de l'ajout : {e}", "error")
            return redirect(url_for('ajouter_client'))

    # Si c'est un GET, on affiche juste le formulaire
    return render_template('ajouter_client.html')

@app.route('/ajouter_documents', methods=['GET', 'POST'])
def ajouter_documents():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    
    db=get_db()

    if request.method=='POST':
        if 'fichier' not in request.files :
            return "Aucun fichier détecté"
        
        file=request.files['fichier']
        id_projet=request.form.get('id_projet')

        if file.filename=='':
            return "Aucun fichier sélectionné"
        
        if file :
            nom_fichier=secure_filename(file.filename)
            sauveguarde=os.path.join('static', 'documents')
            chemin_complet=os.path.join(sauveguarde, nom_fichier)
            file.save(chemin_complet)
            chemin_bdd=f"documents/{nom_fichier}"
            date_upload=date.today()
            id_connecte = session.get('user_id')

            sql="INSERT INTO Documents (idi, idp, type, chemin, upload) VALUES (?, ?, ?, ?, ?)"
            db.execute(sql, (id_connecte, id_projet, 'Autre', chemin_bdd, date_upload))
            db.commit()

            return redirect(url_for('details_projet', id_projet=id_projet))

    projets=db.execute("SELECT idp, titre_projet FROM Projets").fetchall()
    pre_select = request.args.get('id_projet')
    return render_template('ajouter_documents.html', projets=projets, pre_select=pre_select )

def algorythme_matching(id_projet):
    db=get_db()

    sql_projet="SELECT p.*, c.secteur FROM Projets p LEFT JOIN Clients c ON p.idc=c.idc WHERE p.idp=?"
    projet_cible=db.execute(sql_projet, (id_projet,)).fetchone()

    if not projet_cible:
        return []
    
    if projet_cible['etat'] != 'En attente':
        return []

    secteur_vise=projet_cible['secteur']

    valeur_niveau={ 'Debutant':1, 'Intermédiaire':2, 'Avancé':3, 'Expert':4 }
    sql_besoins="SELECT idcomp, niveau_requis FROM ProjetNecessite WHERE idp=?"
    rows_besoins=db.execute(sql_besoins, (id_projet,)).fetchall()
    
    besoins_dict={}
    for row in rows_besoins:
        niveau_clean = row['niveau_requis'] if row['niveau_requis'] else 'Debutant'
        besoins_dict[row['idcomp']] = valeur_niveau.get(niveau_clean, 1)
    
    intervenants=db.execute("SELECT idi, nom, prenom, dispo FROM Intervenants")
    resultats=[]

    for personne in intervenants:
        if personne['dispo'] != 'Oui':
            continue
        idi=personne['idi']
        score=0
        details=[]
        if besoins_dict:
            sql_skills="SELECT idcomp, niveau FROM PossedeCompetence WHERE idi=?"
            competences=db.execute(sql_skills, (idi,)).fetchall()
            for competence in competences:
                idcomp=competence['idcomp']
                if idcomp in besoins_dict:
                    niveau_requis=besoins_dict[idcomp]
                    niveau_possede=valeur_niveau.get(competence['niveau'],1)
                    nom_comp=db.execute('SELECT competence FROM Competences WHERE idcomp=?', (idcomp,)).fetchone()[0]
                    if niveau_possede >= niveau_requis:
                        score+=20
                        details.append(f"Competence validée: {nom_comp}")
                    else :
                        score+=10
                        details.append(f"Competence acquise mais niveau juste: {nom_comp}")

        sql_exp="SELECT p.titre_projet, c.secteur FROM Participation pa LEFT JOIN Projets p ON pa.idp=p.idp LEFT JOIN Clients c on p.idc=c.idc WHERE pa.idi=? AND p.etat='Terminé'"
        historique=db.execute(sql_exp, (idi,)).fetchall()
        nbProjetMmSecteur=0
        for ancienp in historique :
            if ancienp['secteur']==secteur_vise:
                score+=15
                nbProjetMmSecteur+=1
                details.append(f"Expert dans le secteur {secteur_vise} grâce a l'ancien projet {ancienp['titre_projet']}")
            else :
                score+=5
                details.append(f"Bonus d'experience")

        if score>0:
            resultats.append({
                'idi':idi, 
                'nom_complet':f"{personne['prenom']} {personne['nom']}", 
                'score':score,
                'details':details,
            })
    return sorted(resultats, key=lambda x: x['score'], reverse=True)



if __name__ == '__main__':
    app.run(debug=True)
