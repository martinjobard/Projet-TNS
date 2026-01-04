import pytest
from tests.conftest import login, logout

def test_page_connexion(client):
    """Vérifie que la page de login s'affiche bien"""
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Connexion" in response.data

def test_login_admin_reussi(client):
    """Teste si l'admin peut se connecter"""
    response = login(client, 'admin_test', 'password123')
    assert response.status_code == 200
    # Vérifie un élément présent seulement quand on est connecté
    assert b"Deconnexion" in response.data or b"Mon compte" in response.data

def test_login_rate(client):
    """Teste qu'on ne peut pas se connecter avec un mauvais mot de passe"""
    
    # 1. On envoie les mauvaises données
    response = client.post('/login', data={
        'identifiant': 'admin_test', 
        'mot_de_passe': 'mauvais_mdp'
    }, follow_redirects=True)

    # 2. On vérifie que la page s'affiche bien (Code 200)
    # C'est important car ton code fait un 'return render_template', pas une redirection.
    assert response.status_code == 200

    # 3. VERIFICATION DU CONTENU HTML
    # Ton code Python envoie la variable erreur="Identifiant ou mot de passe incorrect."
    # Si ton fichier HTML contient {{ erreur }}, ce texte sera présent sur la page.
    
    # On décode la page pour pouvoir lire le texte (y compris les accents)
    page_content = response.data.decode('utf-8')
    
    # On vérifie que la phrase exacte définie dans ton app.py est présente
    assert "Identifiant ou mot de passe incorrect" in page_content

def test_access_page_clients_sans_login(client):
    """Vérifie qu'on est redirigé si on n'est pas connecté"""
    logout(client)
    response = client.get('/Clients', follow_redirects=True)
    assert b"Veuillez vous connecter" in response.data or b"Connexion" in response.data

def test_ajout_client_admin(client):
    """Teste l'ajout d'un client"""
    # 1. Connexion
    login(client, 'admin_test', 'password123')

    # 2. Envoi du formulaire
    client.post('/ajouter_client', data={
        'nom': 'Dupont',
        'prenom': 'Jean',
        'entreprise': 'Test Company',
        'secteur': 'IT',
        'email': 'jean@test.com',
        'telephone': '0606060606',
        'adresse': '1 rue de la Paix, Paris'
    }, follow_redirects=True)

    # 3. VERIFICATION VIA LA SESSION (Comme pour le login)
    with client.session_transaction() as session:
        flash_messages = session.get('_flashes', [])
        messages_texte = [msg for categorie, msg in flash_messages]
        
        # On cherche un message qui confirme le succès
        # On cherche si "Test Company" (le nom de l'entreprise) est cité dans un message
        succes = False
        for msg in messages_texte:
            if "Test Company" in msg:
                succes = True
                break
        
        assert succes, f"Le message de confirmation n'a pas été trouvé. Messages reçus : {messages_texte}"