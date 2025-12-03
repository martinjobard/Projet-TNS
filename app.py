from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, url_for, session, redirect, g
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
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

DATABASE= "ppii.db"


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
    return render_template('Projets.html', titre=titre_site)

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
    return render_template('Stats.html', titre=titre_site)

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
    titre_site = "Site interne TNS"
    return render_template('Mon_compte.html', titre=titre_site)

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
        
        db = sqlite3.connect('ppii.db')
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
            
            db = sqlite3.connect('ppii.db')
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

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/Intervenants/<nomcomplet>')
def Inter_profil(nomcomplet=None):
    db = get_db()
    c = db.cursor()
    [name, surname]=nomcomplet.split('.')
    sql = "SELECT nom, prénom FROM Clients nom=? AND prénom=?"
    c.execute(sql, (name, surname))
    selected_students = c.fetchone() #plus trouver les compétences 
    if selected_students is None:
       return render_template("error_intervenants.html", message="Intervenant non trouvé")
    return render_template('Intervenant_profil.html', nom=selected_students['nom'], prénom=selected_students['prénom'] )