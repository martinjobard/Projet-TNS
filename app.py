from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, url_for, session, redirect, g, Response
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
import unicodedata
import json
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



@app.route('/')
def Accueil():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    return render_template('Accueil.html', titre=titre_site)

@app.route('/Clients')
def Clients():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    return render_template('Clients.html', titre=titre_site)

@app.route('/Projets')
def Projets():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"

    db=get_db()
    sql="""
    SELECT p.idp, p.etat, c.nom as Nom_Client
    FROM Projets p LEFT JOIN Clients c ON p.idc=c.idc
    """
    liste_projets=db.execute(sql).fetchall()
    total_projets=len(liste_projets)
    liste_en_cours=[p for p in liste_projets if p['etat']=='En cours']
    liste_termines=[p for p in liste_projets if p['etat']=='Terminé']
    return render_template('Projets.html', titre=titre_site, tous_les_projets=liste_projets, projets_en_cours=liste_en_cours, projets_termines=liste_termines)

@app.route('/Intervenants')
def Intervenants():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    return render_template('Intervenants.html', titre=titre_site)

@app.route('/Import-Export')
def Import_Export():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    return render_template('Import_Export.html', titre=titre_site)

@app.route('/Wiki-Docs')
def Wiki_Docs():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    return render_template('Wiki_Docs.html', titre=titre_site)

@app.route('/tinder_like')
def tinder_like():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    return render_template('tinder_like.html', titre=titre_site)

@app.route('/Stats')
def Stats():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    return render_template(
        "Stats.html",
        nb_clients=42,
        nb_projects=6,
        ca="52 000 €",

        monthly_labels=["Jan", "Fév", "Mar", "Avr"],
        monthly_projects=[3, 2, 7, 5],

        sector_labels=["Tech", "Énergie", "Santé"],
        sector_values=[12, 8, 5],

        table_data=[
            {
                "client": "EDF",
                "sector": "Énergie",
                "project": "SmartGrid",
                "status": "En cours",
                "date": "2025-12-01"
            }
        ]
    )

@app.route('/Missions_réalisées')
def Missions_réalisées():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    return render_template('Missions_réalisées.html', titre=titre_site)

@app.route('/Partenaires')
def Partenaires():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    return render_template('Partenaires.html', titre=titre_site)

@app.route('/Contact')
def Contact():
    redirect_if_needed = require_login()
    if redirect_if_needed:
        return redirect_if_needed
    titre_site = "Site interne TNS"
    return render_template('Contact.html', titre=titre_site)

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
        I.nom, 
        I.prenom 
    FROM Utilisateur_Intervenant UI
    JOIN Intervenants I ON UI.idi = I.idi 
    WHERE UI.nom_utilisateur = ?
    """
    
    c.execute(sql, (username,))
    data = c.fetchone()

    # Initialisation des variables
    nom_compte = "Inconnu"
    email = "Inconnu"
    pdp_url = None
    lien_formatte = None # C'est la variable pour ton URL

    if data:
        # 1. Infos du compte utilisateur
        nom_compte = (data['nom_utilisateur'])
        email = data['email_utilisateur']
        pdp_url = data['pdp_url']
        
        # 2. Infos de l'intervenant pour construire le lien
        # On vérifie que les champs existent bien
        if data['nom'] and data['prenom']:
            nom_reel = normalize_text(data['nom'])
            prenom_reel = normalize_text(data['prenom'])
            # On formate : "Nom.Prenom" pour que la route Inter_profil puisse faire le split('.')
            lien_formatte = f"{nom_reel}.{prenom_reel}"
    
    return render_template('Mon_compte.html', 
        nom_utilisateur=nom_compte, 
        email_utilisateur=email,
        pdp_actuelle=pdp_url,
        lien_intervenant=lien_formatte # <--- C'est la nouvelle variable importante !
    )

# --- NOUVELLES ROUTES (Ajoute ceci avant le if __name__ == '__main__':) ---

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
    return render_template('Connexion.html', titre=titre_site)

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
        sql = "SELECT mdp_haché, pdp_url FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?"
        c.execute(sql, (username,))
        result = c.fetchone()
        db.close()
        if result:
            mdp_hash = result[0]
            pdp_url = result[1]
        else:
            mdp_hash = None
            pdp_url = None
        
        if mdp_hash and check_password_hash(mdp_hash, password):
            # Succès ! Stocker les informations
            session['logged_in'] = True
            session['username'] = username
            session['pdp_url'] = pdp_url # ⬅️ NOUVEAU : On stocke l'URL dans la session !
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
        sql = "SELECT nom_utilisateur, email_utilisateur, pdp_url FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?"
        c.execute(sql, (username,))
        user_row = c.fetchone()
        
        db.close()

        if user_row:
            # 2. Création du dictionnaire de données
            donnees = {
                "profil": {
                    "nom_utilisateur": user_row['nom_utilisateur'],
                    "email": user_row['email_utilisateur'],
                    "photo_profil": user_row['pdp_url']
                },
                "statut": "Actif",
                "date_export": "Aujourd'hui" # Tu pourrais utiliser datetime.now() ici
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
        db = sqlite3.connect(DATABASE)
        c = db.cursor()
        
        # Suppression de l'utilisateur
        sql = "DELETE FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?"
        c.execute(sql, (username,))
        db.commit()
        db.close()
        
        # IMPORTANT : On vide la session (déconnexion forcée)
        session.clear()
        
        # On redirige vers l'accueil ou la connexion avec un message (optionnel)
        return redirect(url_for('Connexion'))
        
    except Exception as e:
        return f"Erreur lors de la suppression : {e}"




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
        I.nom, 
        I.prenom, 
        C.competence, 
        PC.niveau 
    FROM Intervenants I
    LEFT JOIN PossedeCompetence PC ON I.idi = PC.idi
    LEFT JOIN Competences C ON C.idcomp = PC.idcomp
    WHERE I.nom = ? AND I.prenom = ?
    """
    
    c.execute(sql, (name_search, surname_search))
    rows = c.fetchall()

    # 4. Vérification : Si la liste est vide, c'est que la personne n'existe vraiment pas
    if not rows:
       return render_template("error_intervenant.html", message="Intervenant non trouvé")

    # 5. On récupère les infos de base (sur la première ligne)
    nom_affiche = normalize_text(rows[0]['nom'])
    prenom_affiche = normalize_text(rows[0]['prenom'])
    
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
                           nom=nom_affiche, 
                           prenom=prenom_affiche, 
                           competences=competences)



if __name__ == '__main__':
    app.run(debug=True)



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
        C.nom, 
        C.prenom, 
        C.secteur, 
        C.telephone,
        C.email,
        C.dernier_contact,
        P.idp,
        P.etat

    FROM Clients C
    LEFT JOIN Projet P ON C.idc = P.idc
    WHERE C.nom = ? AND C.prenom = ?
    """
    
    c.execute(sql, (name_search, surname_search))
    rows = c.fetchall()

    # 4. Vérification : Si la liste est vide, c'est que la personne n'existe vraiment pas
    if not rows:
       return render_template("error_client.html", message="Nous n'avons pas encore travaillé avec cette personne, vérifiez peut-être l'orthographe ")

    # 5. On récupère les infos de base (sur la première ligne)
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

    return render_template('Client_profil.html', 
                           nom=nom_affiche, 
                           prenom=prenom_affiche, 
                           secteur=secteur,
                           telephone=telephone,
                           dernier_contact=dernier_contact,
                           email=email,
                           projets=projets)

