
PRAGMA foreign_keys = ON;

-- ------------------------------
-- Clients (Parents)
-- ------------------------------
INSERT INTO Clients (idc, nom, prenom, email, telephone, secteur, dernier_contact, nom_entreprise, adresse, lattitude, longitude) VALUES
(1, 'jobart', 'alice', 'alice@techcorp.com', '0123456789', 'IT', '2025-11-20', 'TechCorp', '55 Rue du Faubourg Saint-Honoré, 75008 Paris', 48.87062, 2.31693),
(2, 'cipres', 'bob', 'bob@innov.com', '0987654321', 'Finance', '2025-12-01', 'InnovSolutions', '10 Rue de la République, 69002 Lyon', 45.76014, 4.83556),
(3, 'dubois', 'charlie', 'charlie@green.org', '0611223344', 'Environnement', '2025-10-15', 'GreenFuture', '3 Avenue des Champs-Élysées, 75008 Paris', 48.8698, 2.3075);

-- ------------------------------
-- Intervenants (Parents)
-- ------------------------------
INSERT INTO Intervenants (idi, role, nb_heure, dispo, nom, prenom, date_inscription) VALUES
(101, 'Président', 35, 'Oui', 'dubois', 'marc', '2024-09-02'),
(102, 'Développeur Senior', 30, 'Oui', 'lefevre', 'sophie', '2025-12-11'),
(103, 'Designer UX/UI', 20, 'Non', 'martin', 'pierre', '2025-03-05'),
(104, 'Consultant', 40, 'Oui', 'bernard', 'julie', '2024-02-11');

-- ------------------------------
-- Compétences (Parents)
-- ------------------------------
INSERT INTO Competences (idcomp, competence) VALUES
(1, 'Python'),
(2, 'SQL'),
(3, 'JavaScript'),
(4, 'Figma'),
(5, 'Gestion de Projet'),
(6, 'Cloud AWS');

-- ------------------------------
-- Projets (Référence Clients)
-- ------------------------------
INSERT INTO Projets (idp, idc, etat, budget, deb, fin, titre_projet) VALUES
(1001, 1, 'En cours', 50, '20/12/2022', '', 'Création de plateforme e-commerce'),
(1002, 2, 'Terminé', 80, '03/04/2024', '18/07/2025', 'Développement application mobile iOS'),
(1003, 1, 'En attente', 500, '', '', 'Site Boulangerie'),
(1004, 3, 'En cours', 99, '12/09/2025', '', 'Audit de sécurité réseau interne');

-- ------------------------------
-- Participation (Référence Projets et Intervenants)
-- ------------------------------
INSERT INTO Participation (idp, idi, role) VALUES
(1001, 101, 'Chef'),
(1001, 102, 'Dev'),
(1002, 104, 'Consultant'),
(1004, 103, 'Designer'),
(1004, 101, 'Assistant');

-- ------------------------------
-- PossedeCompetence (Référence Intervenants et Compétences)
-- ------------------------------
INSERT INTO PossedeCompetence (idi, idcomp, niveau) VALUES
(101, 5, 'Expert'),
(101, 2, 'Intermédiaire'),
(102, 1, 'Expert'),
(102, 3, 'Avancé'),
(103, 4, 'Expert'),
(104, 6, 'Avancé');

-- ------------------------------
-- Utilisateur_Intervenant (Référence Intervenants)
-- ------------------------------
INSERT INTO Utilisateur_Intervenant (idu, mdp_haché, idi, nom_utilisateur, pdp_url, email_utilisateur,fonction,status) VALUES
(501, 'scrypt:32768:8:1$MOtMqccFPxmGG8Dv$3bc6e0c780e3a3c4901db9ae099eaf7233293a3c2a2dfac869f8ca7f6d8655a56d95eb4384a9662154473d786c01601aaebadaabad359be8ad39e5db5fa4230a', 101, 'marc_d', 'images/profiles/marc_d.png', 'marc@interv.com', 'admin',1),
(502, 'scrypt:32768:8:1$9uGypIgiLHFN5Kh5$45286b231659b83a8338e9df56583afc7776f60a8c695e042bdfef6a2b8ebf33d13623ce2a24d7406bf14af5d9ca009da7f6a6db527e7aed678d840450fb062b', 102, 'sophie_l', 'images/profiles/sophie_l.png', 'sophie@interv.com','user',1);

-- ------------------------------
-- Historique (Référence Clients et Intervenants)
-- ------------------------------
INSERT INTO Historique (idh, date, idc, idi, interaction_text) VALUES
(10001, '2025-12-05', 1, 101, 'Appel de suivi projet 1001'),
(10002, '2025-11-25', 2, 104, 'Envoi du rapport final pour projet 1002'),
(10003, '2025-10-16', 3, 101, 'Premier contact pour définir le cahier des charges');

-- ------------------------------
-- Documents (Référence Intervenants et Projets)
-- ------------------------------
INSERT INTO Documents (idDoc, idi, idp, type, chemin, upload) VALUES
(2001, 101, 1002, 'CR1 PPII', 'documents/CR_PPII_24_11_25__.pdf', '2025-11-24'),
(2002, 102, 1002, 'CR2 PPII', 'documents/CR_PPII_01_12_25.pdf', '2025-12-01');
