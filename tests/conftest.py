import pytest
import os
import sys
import tempfile
import shutil
import sqlite3
from werkzeug.security import generate_password_hash

# Ajout du chemin pour trouver l'application
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, get_db

NOM_FICHIER_DB_TEST = 'gestion_projets_test.db'

def init_db_if_empty(db_path):
    """Vérifie si la table Utilisateur_Intervenant existe, sinon lance le schema.sql"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # On teste sur la VRAIE table de ton schéma
        cursor.execute("SELECT * FROM Utilisateur_Intervenant LIMIT 1")
    except sqlite3.OperationalError:
        print("⚠️ Tables manquantes. Initialisation via schema.sql...")
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                conn.executescript(f.read())
            conn.commit()
            print("✅ Tables créées avec succès !")
        else:
            print("❌ ERREUR : schema.sql introuvable")
    conn.close()

@pytest.fixture
def client():
    # 1. Gestion du fichier de BDD
    master_db_path = os.path.join(os.path.dirname(__file__), '..', NOM_FICHIER_DB_TEST)
    if not os.path.exists(master_db_path):
        open(master_db_path, 'a').close()

    # 2. Auto-réparation si vide
    init_db_if_empty(master_db_path)

    # 3. Copie temporaire (Isolation)
    db_fd, temp_db_path = tempfile.mkstemp()
    shutil.copy2(master_db_path, temp_db_path)

    app.config['TESTING'] = True
    app.config['DATABASE'] = temp_db_path

    with app.test_client() as client:
        with app.app_context():
            db = get_db()
            
            # --- CRÉATION DE L'ADMIN DE TEST (ADAPTÉ À TON SCHÉMA) ---
            
            # 1. On nettoie l'existant (pour éviter les doublons si le test relance)
            try:
                # On récupère l'ID de l'intervenant lié à l'admin pour le supprimer aussi
                cur = db.execute("SELECT idi FROM Utilisateur_Intervenant WHERE nom_utilisateur = 'admin_test'")
                row = cur.fetchone()
                if row:
                    idi_admin = row['idi']
                    db.execute("DELETE FROM Utilisateur_Intervenant WHERE nom_utilisateur = 'admin_test'")
                    db.execute("DELETE FROM Intervenants WHERE idi = ?", (idi_admin,))
                    db.commit()
            except Exception:
                pass 

            # 2. CRÉATION OBLIGATOIRE D'UN INTERVENANT (Car clé étrangère idi)
            # On insère d'abord un intervenant fictif pour l'admin
            cur = db.execute(
                "INSERT INTO Intervenants (nom, prenom, role, nb_heure, dispo, date_inscription) VALUES (?, ?, ?, ?, ?, ?)",
                ('ADMIN', 'System', 'Administrateur', 0, 'Non', '2025-01-01')
            )
            id_intervenant = cur.lastrowid # On récupère l'ID généré (idi)

            # 3. CRÉATION DE L'UTILISATEUR (Lié à l'intervenant créé au-dessus)
            # Note : Ta colonne mot de passe s'appelle 'mdp_haché' dans ton schéma !
            db.execute(
                """
                INSERT INTO Utilisateur_Intervenant 
                (idi, nom_utilisateur, mdp_haché, fonction, email_utilisateur, pdp_url, status) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (id_intervenant, 'admin_test', generate_password_hash('password123'), 'admin', 'admin@test.com', 'default.png', 1)
            )
            db.commit()
            
        yield client

    # 4. Nettoyage
    os.close(db_fd)
    os.unlink(temp_db_path)

# --- HELPER DE CONNEXION ---
def login(client, username, password):
    # Ici on garde les names de ton HTML (identifiant / mot_de_passe)
    # Ton code Python (app.py) fera le lien avec la BDD
    return client.post('/login', data={
        'identifiant': username,    
        'mot_de_passe': password    
    }, follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)