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
    assert b"Deconnexion" in response.data or b"Mon compte" in response.data

def test_login_rate(client):
    """Teste qu'on ne peut pas se connecter avec un mauvais mot de passe"""
    
    response = client.post('/login', data={
        'identifiant': 'admin_test', 
        'mot_de_passe': 'mauvais_mdp'
    }, follow_redirects=True)

    assert response.status_code == 200

    
    page_content = response.data.decode('utf-8')
    
    assert "Identifiant ou mot de passe incorrect" in page_content

def test_access_page_clients_sans_login(client):
    """Vérifie qu'on est redirigé si on n'est pas connecté"""
    logout(client)
    response = client.get('/Clients', follow_redirects=True)
    assert b"Veuillez vous connecter" in response.data or b"Connexion" in response.data

def test_ajout_client_admin(client):
    """Teste l'ajout d'un client"""
    login(client, 'admin_test', 'password123')

    client.post('/ajouter_client', data={
        'nom': 'Dupont',
        'prenom': 'Jean',
        'entreprise': 'Test Company',
        'secteur': 'IT',
        'email': 'jean@test.com',
        'telephone': '0606060606',
        'adresse': '1 rue de la Paix, Paris'
    }, follow_redirects=True)

    with client.session_transaction() as session:
        flash_messages = session.get('_flashes', [])
        messages_texte = [msg for categorie, msg in flash_messages]
        
        succes = False
        for msg in messages_texte:
            if "Test Company" in msg:
                succes = True
                break
        
        assert succes, f"Le message de confirmation n'a pas été trouvé. Messages reçus : {messages_texte}"