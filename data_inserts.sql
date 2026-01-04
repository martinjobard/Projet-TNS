PRAGMA foreign_keys = ON;

-- ============================================================
-- 1. CLIENTS (Existants + Nouveaux)
-- ============================================================
INSERT INTO Clients (idc, nom, prenom, email, telephone, secteur, dernier_contact, nom_entreprise, adresse, lattitude, longitude) VALUES
-- Existants
(1, 'jobart', 'alice', 'alice@techcorp.com', '0123456789', 'IT', '2025-11-20', 'TechCorp', '55 Rue du Faubourg Saint-Honoré, 75008 Paris', 48.87062, 2.31693),
(2, 'cipres', 'bob', 'bob@innov.com', '0987654321', 'Finance', '2025-12-01', 'InnovSolutions', '10 Rue de la République, 69002 Lyon', 45.76014, 4.83556),
(3, 'dubois', 'charlie', 'charlie@green.org', '0611223344', 'Environnement', '2025-10-15', 'GreenFuture', '3 Avenue des Champs-Élysées, 75008 Paris', 48.8698, 2.3075),
-- Nouveaux (Données variées pour tests)
(4, 'martin', 'lucas', 'lucas.martin@immo.fr', '0655443322', 'Immobilier', '2025-12-10', 'ImmoPlus', '12 Place du Capitole, 31000 Toulouse', 43.6045, 1.4442),
(5, 'petit', 'julie', 'j.petit@fashion.com', '0788996655', 'Mode', '2025-09-12', 'ModeParis', '45 Rue de Rivoli, 75001 Paris', 48.8590, 2.3420),
(6, 'roux', 'thomas', 't.roux@agro.com', '0612341234', 'Agroalimentaire', '2025-11-05', 'BioFerme', '8 Rue Sainte-Catherine, 33000 Bordeaux', 44.8404, -0.5805),
(7, 'durand', 'emma', 'emma.d@logistique.net', '0698765432', 'Logistique', '2025-10-30', 'SpeedLog', '22 Boulevard Carnot, 59000 Lille', 50.6365, 3.0635),
(8, 'leroy', 'nicolas', 'nico.leroy@btp.org', '0711223344', 'BTP', '2025-12-12', 'ConstructAll', '5 Quai de la Joliette, 13002 Marseille', 43.3026, 5.3691),
(9, 'moreau', 'sarah', 'sarah.m@sante.fr', '0622334455', 'Santé', '2025-11-28', 'MediCare', '15 Rue de Verdun, 44000 Nantes', 47.2184, -1.5536),
(10, 'simon', 'alexandre', 'alex.simon@auto.com', '0633445566', 'Automobile', '2025-08-20', 'AutoDrive', '10 Avenue Jean Médecin, 06000 Nice', 43.7009, 7.2683),
(11, 'laurent', 'chloe', 'chloe.l@education.gouv', '0644556677', 'Éducation', '2025-09-01', 'EdTech France', '2 Rue de la Paix, 67000 Strasbourg', 48.5839, 7.7455),
(12, 'michel', 'david', 'david.m@energy.com', '0655667788', 'Énergie', '2025-12-05', 'SolarSystem', '7 Place Royale, 35000 Rennes', 48.1113, -1.6800),
(13, 'garcia', 'laura', 'laura.g@art.com', '0666778899', 'Culture', '2025-11-15', 'ArtGallery', '9 Rue des Clercs, 57000 Metz', 49.1197, 6.1764),
(14, 'david', 'kevin', 'kevin.d@sport.com', '0777889900', 'Sport', '2025-10-10', 'FitLife', '30 Rue de la Liberté, 21000 Dijon', 47.3216, 5.0415),
(15, 'bertrand', 'oceanne', 'oceanne@startup.io', '0688990011', 'IT', '2025-12-14', 'NextBigThing', 'Technopole Sophia Antipolis, 06560 Valbonne', 43.6167, 7.0500);

-- ============================================================
-- 2. INTERVENANTS (Existants + Nouveaux)
-- ============================================================
INSERT INTO Intervenants (idi, role, nb_heure, dispo, nom, prenom, date_inscription) VALUES
-- Existants
(101, 'Président', 35, 'Oui', 'dubois', 'marc', '2024-09-02'),
(102, 'Développeur Senior', 30, 'Oui', 'lefevre', 'sophie', '2025-12-11'),
(103, 'Designer UX/UI', 20, 'Non', 'martin', 'pierre', '2025-03-05'),
(104, 'Consultant', 40, 'Oui', 'bernard', 'julie', '2024-02-11'),
-- Nouveaux
(105, 'Développeur Junior', 35, 'Oui', 'tessier', 'antoine', '2025-06-15'),
(106, 'Chef de Projet', 39, 'Oui', 'girard', 'elodie', '2025-01-20'),
(107, 'Data Scientist', 25, 'Non', 'fontaine', 'lucas', '2025-08-10'),
(108, 'DevOps', 35, 'Oui', 'chevalier', 'maxime', '2025-05-05'),
(109, 'Consultant SEO', 15, 'Oui', 'gauthier', 'clara', '2025-09-01'),
(110, 'Développeur Mobile', 30, 'Oui', 'perrin', 'nathan', '2025-10-12'),
(111, 'Administrateur Sys', 35, 'Oui', 'robin', 'hugo', '2024-11-30'),
(112, 'Commercial', 40, 'Oui', 'masson', 'lea', '2025-02-28');

-- ============================================================
-- 3. COMPÉTENCES (Existants + Nouvelles)
-- ============================================================
INSERT INTO Competences (idcomp, competence) VALUES
(1, 'Python'),
(2, 'SQL'),
(3, 'JavaScript'),
(4, 'Figma'),
(5, 'Gestion de Projet'),
(6, 'Cloud AWS'),
-- Nouvelles
(7, 'Docker/Kubernetes'),
(8, 'React Native'),
(9, 'Machine Learning'),
(10, 'SEO / Marketing'),
(11, 'Java / Spring'),
(12, 'Cybersécurité');

-- ============================================================
-- 4. PROJETS (Existants + Nouveaux)
-- ============================================================
INSERT INTO Projets (idp, idc, etat, budget, deb, fin, titre_projet) VALUES
-- Existants
(1001, 1, 'En cours', 50, '20/12/2022', '', 'Création de plateforme e-commerce'),
(1002, 2, 'Terminé', 80, '03/04/2024', '18/07/2025', 'Développement application mobile iOS'),
(1003, 1, 'En attente', 500, '', '', 'Site Boulangerie'),
(1004, 3, 'En cours', 99, '12/09/2025', '', 'Audit de sécurité réseau interne'),
-- Nouveaux
(1005, 4, 'En cours', 120, '15/10/2025', '', 'Portail de gestion locative'),
(1006, 5, 'Terminé', 45, '10/01/2025', '20/06/2025', 'Refonte site vitrine Mode'),
(1007, 6, 'En attente', 75, '', '', 'Application traçabilité Bio'),
(1008, 7, 'En cours', 200, '01/11/2025', '', 'Optimisation flotte camions (IA)'),
(1009, 8, 'Annulé', 30, '01/03/2025', '15/04/2025', 'POC Impression 3D'),
(1010, 9, 'En cours', 150, '05/09/2025', '', 'Dossier patient numérique'),
(1011, 10, 'Terminé', 60, '12/02/2025', '30/08/2025', 'Configurateur voiture 3D'),
(1012, 11, 'En cours', 90, '01/10/2025', '', 'Plateforme e-learning'),
(1013, 12, 'En attente', 300, '', '', 'Dashboard consommation énergétique'),
(1014, 15, 'En cours', 500, '01/12/2025', '', 'Développement MVP SaaS');

-- ============================================================
-- 5. PARTICIPATION
-- ============================================================
INSERT INTO Participation (idp, idi, role) VALUES
-- Existants
(1001, 101, 'Chef'),
(1001, 102, 'Dev'),
(1002, 104, 'Consultant'),
(1004, 103, 'Designer'),
(1004, 101, 'Assistant'),
-- Nouveaux
(1005, 106, 'Chef'),
(1005, 105, 'Dev Back'),
(1005, 103, 'Designer'),
(1006, 109, 'SEO'),
(1008, 107, 'Data Scientist'),
(1008, 101, 'Superviseur'),
(1010, 106, 'Chef'),
(1010, 102, 'Dev Lead'),
(1011, 110, 'Dev Mobile'),
(1012, 111, 'Admin Sys'),
(1014, 108, 'DevOps'),
(1014, 105, 'Dev Fullstack');

-- ============================================================
-- 6. POSSEDE COMPETENCE
-- ============================================================
INSERT INTO PossedeCompetence (idi, idcomp, niveau) VALUES
-- Existants
(101, 5, 'Expert'),
(101, 2, 'Intermédiaire'),
(102, 1, 'Expert'),
(102, 3, 'Debutant'),
(103, 4, 'Expert'),
(104, 6, 'Avancé'),
-- Nouveaux
(105, 1, 'Avancé'), -- Antoine (Python)
(105, 3, 'Intermédiaire'), -- Antoine (JS)
(106, 5, 'Expert'), -- Elodie (Gestion)
(107, 1, 'Expert'), -- Lucas (Python)
(107, 9, 'Expert'), -- Lucas (ML)
(108, 7, 'Avancé'), -- Maxime (Docker)
(108, 6, 'Expert'), -- Maxime (AWS)
(109, 10, 'Expert'), -- Clara (SEO)
(110, 8, 'Expert'), -- Nathan (React Native)
(111, 12, 'Intermédiaire'); -- Hugo (Cyber)

-- ============================================================
-- 7. UTILISATEUR_INTERVENANT (Avec MDP Hachés)
-- ============================================================
-- NOTE: Pour les nouveaux utilisateurs, j'ai copié le hash de 'marc_d' (ID 501).
-- Le mot de passe est donc identique à celui de Marc.
INSERT INTO Utilisateur_Intervenant (idu, mdp_haché, idi, nom_utilisateur, pdp_url, email_utilisateur, fonction, status) VALUES
-- Existants
(501, 'scrypt:32768:8:1$MOtMqccFPxmGG8Dv$3bc6e0c780e3a3c4901db9ae099eaf7233293a3c2a2dfac869f8ca7f6d8655a56d95eb4384a9662154473d786c01601aaebadaabad359be8ad39e5db5fa4230a', 101, 'marc_d', 'images/profiles/marc_d.png', 'marc@interv.com', 'admin', 1),
(502, 'scrypt:32768:8:1$9uGypIgiLHFN5Kh5$45286b231659b83a8338e9df56583afc7776f60a8c695e042bdfef6a2b8ebf33d13623ce2a24d7406bf14af5d9ca009da7f6a6db527e7aed678d840450fb062b', 102, 'sophie_l', 'images/profiles/sophie_l.png', 'sophie@interv.com', 'user', 1),
-- Nouveaux
(503, 'scrypt:32768:8:1$MOtMqccFPxmGG8Dv$3bc6e0c780e3a3c4901db9ae099eaf7233293a3c2a2dfac869f8ca7f6d8655a56d95eb4384a9662154473d786c01601aaebadaabad359be8ad39e5db5fa4230a', 105, 'antoine_t', 'images/profiles/default.png', 'antoine@interv.com', 'user', 1),
(504, 'scrypt:32768:8:1$MOtMqccFPxmGG8Dv$3bc6e0c780e3a3c4901db9ae099eaf7233293a3c2a2dfac869f8ca7f6d8655a56d95eb4384a9662154473d786c01601aaebadaabad359be8ad39e5db5fa4230a', 106, 'elodie_g', 'images/profiles/default.png', 'elodie@interv.com', 'manager', 1),
(505, 'scrypt:32768:8:1$MOtMqccFPxmGG8Dv$3bc6e0c780e3a3c4901db9ae099eaf7233293a3c2a2dfac869f8ca7f6d8655a56d95eb4384a9662154473d786c01601aaebadaabad359be8ad39e5db5fa4230a', 107, 'lucas_f', 'images/profiles/default.png', 'lucas@interv.com', 'user', 1),
(506, 'scrypt:32768:8:1$MOtMqccFPxmGG8Dv$3bc6e0c780e3a3c4901db9ae099eaf7233293a3c2a2dfac869f8ca7f6d8655a56d95eb4384a9662154473d786c01601aaebadaabad359be8ad39e5db5fa4230a', 108, 'maxime_c', 'images/profiles/default.png', 'maxime@interv.com', 'admin', 1),
(507, 'scrypt:32768:8:1$MOtMqccFPxmGG8Dv$3bc6e0c780e3a3c4901db9ae099eaf7233293a3c2a2dfac869f8ca7f6d8655a56d95eb4384a9662154473d786c01601aaebadaabad359be8ad39e5db5fa4230a', 110, 'nathan_p', 'images/profiles/default.png', 'nathan@interv.com', 'user', 0), -- Compte désactivé pour test
(508, 'scrypt:32768:8:1$MOtMqccFPxmGG8Dv$3bc6e0c780e3a3c4901db9ae099eaf7233293a3c2a2dfac869f8ca7f6d8655a56d95eb4384a9662154473d786c01601aaebadaabad359be8ad39e5db5fa4230a', 103, 'pierre_m', 'images/profiles/default.png', 'pierre@interv.com', 'user', 1),
(509, 'scrypt:32768:8:1$MOtMqccFPxmGG8Dv$3bc6e0c780e3a3c4901db9ae099eaf7233293a3c2a2dfac869f8ca7f6d8655a56d95eb4384a9662154473d786c01601aaebadaabad359be8ad39e5db5fa4230a', 104, 'julie_b', 'images/profiles/default.png', 'julie@interv.com', 'user', 1),
(510, 'scrypt:32768:8:1$MOtMqccFPxmGG8Dv$3bc6e0c780e3a3c4901db9ae099eaf7233293a3c2a2dfac869f8ca7f6d8655a56d95eb4384a9662154473d786c01601aaebadaabad359be8ad39e5db5fa4230a', 109, 'clara_g', 'images/profiles/default.png', 'clara@interv.com', 'user', 1),
(511, 'scrypt:32768:8:1$MOtMqccFPxmGG8Dv$3bc6e0c780e3a3c4901db9ae099eaf7233293a3c2a2dfac869f8ca7f6d8655a56d95eb4384a9662154473d786c01601aaebadaabad359be8ad39e5db5fa4230a', 111, 'hugo_r', 'images/profiles/default.png', 'hugo@interv.com', 'admin', 1),
(512, 'scrypt:32768:8:1$MOtMqccFPxmGG8Dv$3bc6e0c780e3a3c4901db9ae099eaf7233293a3c2a2dfac869f8ca7f6d8655a56d95eb4384a9662154473d786c01601aaebadaabad359be8ad39e5db5fa4230a', 112, 'lea_m', 'images/profiles/default.png', 'lea@interv.com', 'manager', 1);
-- ============================================================
-- 8. HISTORIQUE
-- ============================================================
INSERT INTO Historique (idh, date, idc, idi, interaction_text) VALUES
-- Existants
(10001, '2025-12-05', 1, 101, 'Appel de suivi projet 1001'),
(10002, '2025-11-25', 2, 104, 'Envoi du rapport final pour projet 1002'),
(10003, '2025-10-16', 3, 101, 'Premier contact pour définir le cahier des charges'),
-- Nouveaux
(10004, '2025-12-14', 4, 106, 'Validation du budget prévisionnel'),
(10005, '2025-12-12', 4, 105, 'Présentation maquettes homepage'),
(10006, '2025-11-30', 7, 107, 'Analyse des données logistiques reçues'),
(10007, '2025-12-01', 15, 108, 'Configuration environnement staging AWS');

-- ============================================================
-- 9. DOCUMENTS
-- ============================================================
INSERT INTO Documents (idDoc, idi, idp, type, chemin, upload) VALUES
-- Existants
(2001, 101, 1002, 'CR1 PPII', 'documents/CR_PPII_24_11_25__.pdf', '2025-11-24'),
(2002, 102, 1002, 'CR2 PPII', 'documents/CR_PPII_01_12_25.pdf', '2025-12-01'),
-- Nouveaux
(2003, 106, 1005, 'Cahier des Charges', 'documents/CDC_ImmoPlus_v1.pdf', '2025-10-10'),
(2004, 109, 1006, 'Audit SEO', 'documents/Audit_ModeParis_Final.pdf', '2025-06-20'),
(2005, 107, 1008, 'Dataset Sample', 'documents/data_sample_logistique.csv', '2025-11-02');

-- ============================================================
-- 10. INTERACTION CLIENT
-- ============================================================
INSERT INTO InteractionClient (idic, idc, idp, date_interaction, type_interaction, contenu) VALUES
-- Existants
(3001, 2, 1002, '2025-03-10', 'Réunion', 'Débriefing sur le cahier des charges. Validation des fonctionnalités de paiement.'),
(3002, 1, 1001, '2025-03-15', 'Email', 'Relance concernant les accès au serveur FTP pour commencer le déploiement.'),
(3003, 3, 1004, '2025-03-16', 'Appel', 'Le client demande si on peut ajouter une option multilingue. Devis complémentaire à prévoir.'), 
(3004, 1, 1003, '2025-03-16', 'Appel', 'Le client demande si on peut ajouter une option multilingue. Devis complémentaire à prévoir.'),
-- Nouveaux
(3005, 4, 1005, '2025-11-10', 'Réunion', 'Le client valide le design mais souhaite changer la couleur principale.'),
(3006, 7, 1008, '2025-11-15', 'Email', 'Envoi des accès API pour le tracking des camions.'),
(3007, 15, 1014, '2025-12-10', 'Déjeuner', 'Discussion informelle sur une extension du contrat pour 2026.');

-- ============================================================
-- 11. PROJET NECESSITE
-- ============================================================
INSERT INTO ProjetNecessite (idp, idcomp, niveau_requis) VALUES
-- Existants
(1003, 1, 'Expert'),
(1003, 2, 'Intermédiaire'),
(1003, 3, 'Debutant'),
(1002, 5, 'Avancé'),
-- Nouveaux
(1008, 1, 'Expert'), -- IA Camions demande Python
(1008, 9, 'Expert'), -- IA Camions demande Machine Learning
(1005, 3, 'Avancé'), -- Immo demande JS
(1014, 6, 'Expert'), -- SaaS demande AWS
(1014, 7, 'Avancé'); -- SaaS demande Docker