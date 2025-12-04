from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, url_for, session, redirect, g
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
app = Flask(__name__)


# Vous avez besoin d'une clé secrète pour les sessions (TRÈS IMPORTANT !)
app.config['SECRET_KEY'] = 'ma_cle_secrete_tres_sure_a_changer'

# --- Définition du Gardien ---
def require_login():
    if 'logged_in' not in session:
        return redirect(url_for('Connexion')) 
    return None

# --- Fonctions de Routes Protégées ---

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
        sql = "SELECT mdp_haché FROM Utilisateur_Intervenant WHERE nom_utilisateur = ?"
        c.execute(sql, (username,))
        result = c.fetchone()
        db.close()
        mdp_hash = result[0] if result else None
        if mdp_hash and check_password_hash(mdp_hash, password):
            # 3. Si les informations sont correctes, créer une session utilisateur
            session['logged_in'] = True
            session['username'] = username
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

hach = generate_password_hash("12345")
print(hach)

if __name__ == '__main__':
    app.run(debug=True)

