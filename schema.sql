PRAGMA foreign_keys = ON;

-- Création des tables PARENTS (sans dépendances)

CREATE TABLE Clients (
    idc INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    prenom TEXT,
    email TEXT,
    telephone TEXT,
    secteur TEXT,
    dernier_contact TEXT,
    nom_entreprise TEXT,
    adresse TEXT,
    lattitude REAL,
    longitude REAL
);

CREATE TABLE Intervenants (
    idi INTEGER PRIMARY KEY,
    role TEXT,
    nb_heure INTEGER,
    dispo TEXT, 
    nom TEXT NOT NULL, 
    prenom TEXT,
    date_inscription TEXT
);

CREATE TABLE Competences (
    idcomp INTEGER PRIMARY KEY,
    competence TEXT NOT NULL
);

-- Création des tables ENFANTS (avec dépendances)

CREATE TABLE "Projets" (
    idp INTEGER PRIMARY KEY,
    idc INTEGER,
    etat TEXT,
    budget INTEGER,
    deb TEXT,
    fin TEXT,
    titre_projet TEXT,
    FOREIGN KEY (idc) REFERENCES Clients(idc)
);

CREATE TABLE Participation (
    idp INTEGER,
    idi INTEGER,
    role TEXT,
    PRIMARY KEY (idp,idi),
    FOREIGN KEY (idp) REFERENCES Projets(idp),
    FOREIGN KEY (idi) REFERENCES Intervenants(idi)
);

CREATE TABLE PossedeCompetence (
    idi INTEGER,
    idcomp INTEGER,
    niveau TEXT,
    PRIMARY KEY (idi, idcomp),
    FOREIGN KEY (idi) REFERENCES Intervenants(idi),  
    FOREIGN KEY (idcomp) REFERENCES Competences(idcomp)
);

CREATE TABLE Utilisateur_Intervenant (
    idu INTEGER PRIMARY KEY,
    mdp_haché TEXT,
    idi INTEGER, 
    nom_utilisateur TEXT, 
    pdp_url TEXT, 
    email_utilisateur TEXT,
    fonction TEXT Default 'user',
    status INTEGER DEFAULT 0,
    FOREIGN KEY (idi) REFERENCES Intervenants(idi)  
);

CREATE TABLE Historique (
    idh INTEGER PRIMARY KEY,
    date TEXT,
    idc INTEGER,
    idi INTEGER,
    interaction_text TEXT,
    FOREIGN KEY (idc) REFERENCES Clients(idc),
    FOREIGN KEY (idi) REFERENCES Intervenants(idi)
);

CREATE TABLE Documents (
    idDoc INTEGER PRIMARY KEY,
    idi INTEGER,
    idp INTEGER,
    type TEXT,
    chemin TEXT,
    upload TEXT,
    FOREIGN KEY (idi) REFERENCES Intervenants(idi),
    FOREIGN KEY (idp) REFERENCES Projets(idp)
);

CREATE TABLE ProjetNecessite (
    idp INTEGER,
    idcomp INTEGER,
    niveau_requis TEXT,
    PRIMARY KEY (idp,idcomp),
    FOREIGN KEY (idp) REFERENCES Projets(idp),
    FOREIGN KEY (idcomp) REFERENCES Competences(idcomp)
);

