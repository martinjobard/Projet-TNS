# 📊 Plateforme de Gestion de Projets TNS

Une application web complète de gestion de projets et de ressources humaines, développée pour le réseau **TNS** (Techniciens, Consultants & Professionnels). Cette plateforme facilite la mise en relation entre les clients, les projets et les intervenants via une interface intuitive et des fonctionnalités avancées de matching.

---

## 🎯 Contexte et Objectifs

Ce projet a été développé dans le cadre d'une soutenance finale pour créer une **plateforme interne** permettant de :

- ✅ **Gérer les clients et leurs projets** : Créer, modifier, et suivre des projets avec budget et calendrier
- ✅ **Gérer les intervenants** : Enregistrer les compétences, disponibilités et historique de chaque professionnel
- ✅ **Matcher automatiquement** : Algorithme intelligent recommandant les meilleurs candidats pour chaque projet
- ✅ **Prospecter efficacement** : Interface "Tinder-like" pour explorer les opportunités commerciales
- ✅ **Analyser les données** : Statistiques détaillées sur les projets, clients et équipes
- ✅ **Exporter/Importer** : Gestion flexible des données via CSV et JSON

---

## 🏗️ Architecture Technique

### Backend
- **Framework** : Flask (Python)
- **Base de données** : SQLite3
- **Authentification** : Hachage sécurisé des mots de passe (Werkzeug)
- **Géolocalisation** : API Nominatim (OpenStreetMap) pour localiser les clients

### Frontend
- **Templating** : Jinja2
- **Styling** : CSS personnalisé
- **Interactivité** : JavaScript vanilla
- **Responsive Design** : Interface adaptée à tous les écrans

### Déploiement
- **Containerisation** : Docker & Docker Compose
- **Port** : 5000

---

## 📋 Fonctionnalités Principales

### 1️⃣ **Gestion des Clients**
- Consultation de la liste complète des clients
- Profils détaillés avec secteur d'activité et historique de contact
- Géolocalisation automatique des adresses
- Import/Export de clients en CSV
- Ajout de clients par administrateur

### 2️⃣ **Gestion des Projets**
- Vue globale avec filtrage par statut (En cours, Terminé, En attente)
- Détails complets : budget, dates, équipe assignée
- Gestion des documents liés aux projets
- Historique des interactions clients

### 3️⃣ **Gestion des Intervenants**
- Profils avec compétences et niveaux (Débutant → Expert)
- Statut de disponibilité
- Historique des projets réalisés
- Système de reconnaissance (top réalisateurs, nouveaux inscrits)

### 4️⃣ **Algorithme de Matching** 🤖
Système intelligent d'appariement basé sur :
- **Compétences requises vs disponibles** : +20 pts par compétence validée
- **Niveau de compétence** : +10 pts pour compétences acquises
- **Expérience secteur** : +15 pts pour expérience dans le même secteur
- **Bonus d'expérience** : +5 pts par projet antérieur

**Résultat** : Classement des meilleurs candidats pour chaque projet

### 5️⃣ **Prospection "Tinder-Like"** 💬
- Interface intuitif de swipe pour explorer les clients potentiels
- Affichage du score de match et du classement
- Gestion des likes et rejets
- Gestion des pistes commerciales identifiées

### 6️⃣ **Statistiques et Analytics** 📈
- Nombre de projets et clients par période
- Distribution par secteur (graphique en camembert)
- Graphique mensuel des projets réalisés
- Filtrage par intervenant et année
- Tableau détaillé des missions

### 7️⃣ **Gestion des Utilisateurs**
- **Inscription** avec système de validation admin
- **Profils personnels** : avatar, bio, compétences
- **Modification de compte** : mot de passe, email, nom d'utilisateur
- **Rôles** : User (par défaut) ou Admin (gestion complète)
- **Suppression** avec export des données (RGPD)

### 8️⃣ **Administration** 🔐
- Validation des inscriptions en attente
- Gestion des clients (ajout, suppression)
- Gestion des intervenants (suppression, attribution de rôles)
- Export de données pour chaque utilisateur

### 9️⃣ **Carte Interactive** 🗺️
- Affichage géographique de tous les clients
- Localisation en temps réel avec OpenStreetMap

### 🔟 **Missions Réalisées** ✨
- Portfolio des projets terminés
- Export des résultats en CSV

---

## 📦 Structure du Projet

```
groupe-18-404-error/
├── app.py                      # Application principale Flask
├── requirements.txt            # Dépendances Python
├── schema.sql                  # Schéma de la base de données
├── data_inserts.sql           # Données de test
├── test_bdd.py                # Script d'initialisation BDD
├── Dockerfile                 # Configuration Docker
├── docker-compose.yml         # Orchestration Docker
│
├── templates/                 # Templates HTML (Jinja2)
│   ├── base.html             # Template de base
│   ├── Accueil.html          # Page d'accueil
│   ├── Clients.html          # Liste des clients
│   ├── Projets.html          # Liste des projets
│   ├── Intervenants.html     # Liste des intervenants
│   ├── tinder_like.html      # Interface de prospection
│   ├── Stats.html            # Dashboard analytique
│   ├── carte_clients.html    # Carte interactive
│   ├── Connexion.html        # Authentification
│   ├── Inscription.html      # Système d'inscription
│   ├── Mon_compte.html       # Profil utilisateur
│   └── ... (14 autres templates)
│
├── static/                    # Ressources statiques
│   ├── css/
│   │   └── style.css         # Feuille de style
│   ├── js/
│   │   └── script.js         # JavaScript utilitaires
│   ├── images/
│   │   └── profiles/         # Photos de profil
│   └── documents/            # Documents stockés
│
└── tests/                     # Suite de tests
    ├── test_routes.py        # Tests des routes
    └── conftest.py           # Configuration pytest
```

---

## 🚀 Installation et Utilisation

### Prérequis
- Python 3.12+
- Docker et Docker Compose (optionnel)

### Sans Docker

1. **Cloner le dépôt**
   ```bash
   git clone <url-du-repo>
   cd groupe-18-404-error
   ```

2. **Créer l'environnement virtuel**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialiser la base de données**
   ```bash
   python test_bdd.py
   ```

5. **Lancer l'application**
   ```bash
   python app.py
   ```

6. **Accéder à l'application**
   - URL : `http://localhost:5000`
   - Login test : `marc.dubois` / `mdp`
   - Login test admin : `sophie.lefevre` / `mdp_123`

### Avec Docker

```bash
docker-compose up --build
```

L'application sera disponible à `http://localhost:5000`

---

## 🗄️ Modèle de Données

### Tables Principales

**Clients**
- Informations personnelles et d'entreprise
- Secteur d'activité, contact, géolocalisation

**Intervenants**
- Profil professionnel
- Disponibilité, rôle, date d'inscription

**Projets**
- Titre, budget, dates, état
- Lien avec client et équipe

**Participation**
- Relation many-to-many : Intervenants ↔ Projets
- Rôle de l'intervenant dans le projet

**PossedeCompetence**
- Compétences de chaque intervenant
- Niveaux : Débutant, Intermédiaire, Avancé, Expert

**Utilisateur_Intervenant**
- Authentification sécurisée
- Profil utilisateur, rôle, statut

**Documents**
- Fichiers associés aux projets
- Historique de téléchargement

**Historique**
- Interactions avec les clients
- Swipes de prospection (likes/dislikes)

---

## 🤖 Algorithme de Matching

L'algorithme d'appariement est au cœur de la plateforme. Il évalue chaque intervenant selon :

1. **Analyse des compétences requises** du projet
2. **Vérification des compétences possédées** par l'intervenant
3. **Évaluation des niveaux** (seuil minimum requis)
4. **Historique professionnel** : expérience dans le même secteur
5. **Disponibilité** : seulement les intervenants "disponibles"

**Formule de scoring :**
```
Score = (Compétences validées × 20) 
       + (Compétences partielles × 10)
       + (Projets secteur similaire × 15)
       + (Expérience générale × 5)
```

Résultat : **Classement des candidats** avec détails de matching

---

## 🔐 Sécurité

✅ **Authentification** : Hachage bcrypt des mots de passe  
✅ **Sessions sécurisées** : Clés secrètes et gestion de session  
✅ **Validation de rôles** : Contrôle d'accès admin/utilisateur  
✅ **RGPD** : Export et suppression de données personnelles  
✅ **Validation d'entrées** : Protection contre l'injection SQL (paramétrages)  

---

## 📊 Technologies Utilisées

| Catégorie | Technologies |
|-----------|--------------|
| **Backend** | Flask, SQLite3, Python 3.12 |
| **Frontend** | HTML5, CSS3, JavaScript |
| **ORM** | SQLite3 (requêtes paramétrées) |
| **Authentification** | Werkzeug security |
| **Géolocalisation** | GeoPy + Nominatim |
| **Déploiement** | Docker, Docker Compose |
| **Testing** | Pytest |
| **Format de données** | JSON, CSV |

---

## 📈 Métriques et Fonctionnalités Clés

- **20+ routes** pour différentes fonctionnalités
- **9 tables** normalisées en base de données
- **1 algorithme intelligent** de matching basé sur compétences
- **100% responsive** : desktop, tablet, mobile
- **Gestion RGPD** complète : export, suppression
- **Interface admin** pour validation et modération

---

## 🎨 Points Forts du Projet

🌟 **Architecture modulaire** : Séparation claire entre routes, données, et présentation  
🌟 **UX intuitive** : Interface "Tinder-like" pour la prospection  
🌟 **Algorithme intelligent** : Matching basé sur 4 critères différents  
🌟 **Scalabilité** : Prêt pour migration vers une vraie DB (PostgreSQL)  
🌟 **Documentation** : Code commenté et structure claire  
🌟 **Conformité RGPD** : Export et suppression de données  

---

## 🔄 Routes API Principales

### Authentification
- `GET/POST /Connexion` - Page de connexion
- `POST /login` - Vérification identifiants
- `GET /logout` - Déconnexion

### Données
- `GET /Clients` - Liste des clients
- `GET /Projets` - Liste des projets
- `GET /Intervenants` - Liste des intervenants
- `GET /Stats` - Tableau de bord statistique

### Prospection
- `GET /tinder_like` - Interface de swipe
- `POST /save_swipe` - Enregistrement d'un like/dislike
- `GET /carte_clients` - Carte interactive

### Profils
- `GET /Clients/<nom.prenom>` - Profil client
- `GET /Intervenants/<nom.prenom>` - Profil intervenant
- `GET /Mon_compte` - Mon profil

### Administration
- `GET /admin/utilisateurs_en_attente` - Validation inscriptions
- `POST /ajouter_client` - Ajout client (admin)
- `POST /modifier_disponibilite` - Mise à jour disponibilité

---

## 🧪 Tests

Exécuter les tests :
```bash
pytest tests/
```

---

## 👨‍💻 Développement et Améliorations Futures

### Potentielles évolutions
- 🔄 Migration vers PostgreSQL pour production
- 📧 Système de notifications email
- 📱 Application mobile
- 🔐 OAuth2 / Single Sign-On
- 🌍 Support multilingue
- 📊 Export Power BI / Tableau

---

## 📝 License

Projet académique - Tous droits réservés

---

## 👤 Auteurs

**Martin** - Etudiant en école d'ingénieur informatique, promo 2028 Telecom Nancy
**Anaelle** - Etudiante en école d'ingénieur informatique, promo 2028 Telecom Nancy
**Mathilde** - Etudiante en école d'ingénieur informatique, promo 2028 Telecom Nancy
**Moran** - Etudiant en école d'ingénieur informatique, promo 2028 Telecom Nancy

---

**Dernier commit** : 19 février 2026