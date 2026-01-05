import sqlite3
import os

DB_NAME = 'gestion_projets_test.db'
SCHEMA_FILE = 'schema.sql' 
DATA_FILE = 'data_inserts.sql'  

def load_sql_from_file(filename):
    """Lit le contenu d'un fichier SQL."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Le fichier '{filename}' est introuvable. Assurez-vous qu'il est dans le même répertoire.")
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def initialize_database(db_name, schema_sql, data_sql):
    """Crée et initialise la base de données."""
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"🗑️  Ancienne base de données '{db_name}' supprimée.")
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")
        print("✅ Clés étrangères activées.")

        print(f"🛠️ Exécution du schéma ({SCHEMA_FILE})...")
        cursor.executescript(schema_sql)

        print(f"⚙️ Insertion des données de test ({DATA_FILE})...")
        cursor.executescript(data_sql)

        conn.commit()
        print(f"\n✨ Succès! La base de données '{db_name}' a été créée et remplie avec succès.")

    except sqlite3.Error as e:
        print(f"\n❌ Erreur SQLite lors de l'initialisation : {e}")
        if conn:
            conn.rollback() 
    except FileNotFoundError as e:
        print(f"\n❌ Erreur de fichier : {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    try:
        schema_content = load_sql_from_file(SCHEMA_FILE)
        
        data_content = load_sql_from_file(DATA_FILE)
        
        initialize_database(DB_NAME, schema_content, data_content)
        
    except FileNotFoundError:
        pass