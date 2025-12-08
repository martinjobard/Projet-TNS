-- Nettoyage complet (y compris les potentiels noms au singulier des anciens essais)
DROP TABLE IF EXISTS Documents;
DROP TABLE IF EXISTS Historique;
DROP TABLE IF EXISTS Utilisateur_Intervenant;
DROP TABLE IF EXISTS PossedeCompetence;
DROP TABLE IF EXISTS Participation;
DROP TABLE IF EXISTS Projets;
DROP TABLE IF EXISTS Projet; -- Suppression de sécurité
DROP TABLE IF EXISTS Clients;
DROP TABLE IF EXISTS Intervenants;
DROP TABLE IF EXISTS Intervenant; -- Suppression de sécurité
DROP TABLE IF EXISTS Competences;

-- Création des tables PARENTS (sans dépendances)

CREATE TABLE Clients (
     idc INTEGER PRIMARY KEY,
     nom TEXT NOT NULL,
     prenom TEXT,
     email TEXT,
     telephone TEXT,
     secteur TEXT,
     dernier_contact TEXT
);

CREATE TABLE Intervenants (
    idi INTEGER PRIMARY KEY,
    role TEXT,
    nb_heure INTEGER,
    dispo TEXT, 
    nom TEXT NOT NULL, 
    prenom TEXT
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
    budget INTEGER
    FOREIGN KEY (idc) REFERENCES Clients(idc)
);

CREATE TABLE Participation (
    idp INTEGER,
    idi INTEGER,
    role TEXT,
    PRIMARY KEY (idp,idi),
    FOREIGN KEY (idp) REFERENCES Projets(idp),       -- Correction: "Projets" avec un S
    FOREIGN KEY (idi) REFERENCES Intervenants(idi)   -- Correction: "Intervenants" avec un S
);

CREATE TABLE PossedeCompetence (
    idi INTEGER,
    idcomp INTEGER,
    niveau TEXT,
    PRIMARY KEY (idi, idcomp),
    FOREIGN KEY (idi) REFERENCES Intervenants(idi),  -- Correction: "Intervenants" avec un S
    FOREIGN KEY (idcomp) REFERENCES Competences(idcomp)
);

CREATE TABLE Utilisateur_Intervenant (
    idu INTEGER PRIMARY KEY,
    mdp_haché TEXT,
    idi INTEGER, 
    nom_utilisateur TEXT, 
    pdp_url TEXT, 
    email_utilisateur TEXT,
    FOREIGN KEY (idi) REFERENCES Intervenants(idi)   -- Correction: "Intervenants" avec un S
);

CREATE TABLE Historique (
    idh INTEGER PRIMARY KEY,
    date TEXT,
    idc INTEGER,
    idi INTEGER,
    interaction_text TEXT,
    FOREIGN KEY (idc) REFERENCES Clients(idc),
    FOREIGN KEY (idi) REFERENCES Intervenants(idi)   -- Correction: "Intervenants" avec un S
);

CREATE TABLE Documents (
    idDoc INTEGER PRIMARY KEY,
    idi INTEGER,
    idp INTEGER,
    type TEXT,
    chemin TEXT,
    upload TEXT,
    FOREIGN KEY (idi) REFERENCES Intervenants(idi),  -- Correction: "Intervenants" avec un S
    FOREIGN KEY (idp) REFERENCES Projets(idp)        -- Correction: "Projets" avec un S
);