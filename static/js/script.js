// static/js/script.js

/* =========================================
   1. GESTION DES MENUS (Sidebar & Navbar)
   ========================================= */

function toggleSousMenu(e) {
    e.preventDefault();
    var sousMenu = e.target.nextElementSibling;
    
    // Ferme les autres
    var tousLesSousMenus = document.querySelectorAll('.dropdown-content');
    tousLesSousMenus.forEach(function(menu) {
        if (menu !== sousMenu) menu.classList.remove('afficher');
    });

    sousMenu.classList.toggle("afficher");
}

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('afficher')) {
                openDropdown.classList.remove('afficher');
            }
        }
    }
    // Fermeture du menu profil si clic ailleurs
    if (!event.target.matches('.avatar') && !event.target.closest('#monProfilDropdown')) {
        var profileMenus = document.getElementsByClassName("profile-dropdown");
        for (var i = 0; i < profileMenus.length; i++) {
            if (profileMenus[i].classList.contains('active')) {
                profileMenus[i].classList.remove('active');
            }
        }
    }
}

function toggleSidebarItem(element) {
    event.preventDefault();
    var submenu = element.nextElementSibling;
    submenu.style.display = (submenu.style.display === "block") ? "none" : "block";
}

function toggleProfileMenu() {
    var menu = document.getElementById("monProfilDropdown");
    if(menu) menu.classList.toggle("active");
}


/* =========================================
   2. PAGE MON COMPTE (Affichage des blocs)
   ========================================= */
document.addEventListener('DOMContentLoaded', function() {
    // On vérifie d'abord si on est sur la page mon compte en cherchant un des boutons
    const btnModifierProfil = document.getElementById('btn_modifier_profil');
    
    if (btnModifierProfil) {
        // IDs corrigés (avec des tirets bas _ et non &)
        const blocNomEmail = document.getElementById('nom_email_modifier_block');
        const blocMdp = document.getElementById('mdp_modifier_block');
        const blocPdp = document.getElementById('pdp_modifier_block');
        
        const btnModifierMdp = document.getElementById('btn_modifier_mdp');    
        const btnModifierPdp = document.getElementById('btn_modifier_pdp');     

        function toggleBlock(blockToShow) {
            if (!blockToShow) return;
            const isVisible = blockToShow.style.display === 'block';
            
            // On ferme tout d'abord
            if(blocNomEmail) blocNomEmail.style.display = 'none';
            if(blocMdp) blocMdp.style.display = 'none';
            if(blocPdp) blocPdp.style.display = 'none';

            // On ouvre celui demandé s'il était fermé
            if (!isVisible) {
                blockToShow.style.display = 'block';
            }
        }

        btnModifierProfil.addEventListener('click', function(e) {
            e.preventDefault();
            toggleBlock(blocNomEmail);
        });

        if(btnModifierMdp) {
            btnModifierMdp.addEventListener('click', function(e) {
                e.preventDefault();
                toggleBlock(blocMdp);
            });
        }

        if(btnModifierPdp) {
            btnModifierPdp.addEventListener('click', function(e) {
                e.preventDefault();
                toggleBlock(blocPdp);
            });
        }
    }
});


/* =========================================
   3. PAGE TINDER (Logique isolée)
   ========================================= */
// On met tout dans un bloc qui ne s'exécute que si le container existe
const tinderContainer = document.getElementById("card-container");

if (tinderContainer) { // <--- C'est cette ligne qui empêche le crash sur les autres pages !
    let isDragging = false;
    let startX = 0;
    let currentCard = null;

    const cardColors = ["#7a1414ff", "#049504ff", "#21217bff", "#d7d724ff", "#2ba3a3ff", "#b10cb1ff", "#b37503ff", "#800080", "#d86666ff", "#262424ff"];

    function createCards() {
        if (typeof dbClients === 'undefined' || dbClients.length === 0) {
            console.log("Aucun client trouvé dans la BDD");
            return;
        }
        
        dbClients.forEach((client, index) => {
            const card = document.createElement("div");
            card.className = "card";
            card.style.backgroundColor = cardColors[index % cardColors.length];
            
            
            card.dataset.clientId = client.id; 
            const cardContent = document.createElement("div"); 
            cardContent.className = "card-content";
            
            
            cardContent.innerHTML = `
            <div class="tinder-inner-content">
                
                <h2 class="tinder-company-name">${client.nom}</h2>
                <p class="tinder-sector">${client.secteur}</p>
                
                <div class="tinder-stats-box">
                    <p class="tinder-rank-score">
                        Rang #${client.mon_rang !== undefined ? client.mon_rang : '-'} &nbsp;|&nbsp; Score : ${client.mon_score || 0}
                    </p>
                    <p class="tinder-project-name">
                        ${client.projet_concerne || 'Projet non spécifié'}
                    </p>
                </div>

            </div>
        `;

            card.appendChild(cardContent);
            tinderContainer.appendChild(card);
        });
    }

    createCards();

    function getTopCard(){
        return tinderContainer.querySelector(".card:last-child");
    }

    // --- Events Souris ---
    tinderContainer.addEventListener("mousedown", (e) => {
        currentCard = getTopCard();
        if (!currentCard) return;
        isDragging = true;
        startX = e.clientX;
        currentCard.style.transition = "none";
    });

    tinderContainer.addEventListener("mousemove", (e) => {
        if(!isDragging || !currentCard) return;
        const deltaX = e.clientX - startX;
        currentCard.style.transform = `translateX(${deltaX}px) rotate(${deltaX/10}deg)`;
    });

    tinderContainer.addEventListener("mouseup", (e) => {
        if(!isDragging || !currentCard) return;
        const deltaX = e.clientX - startX;
        handleSwipe(deltaX);
        isDragging = false;
    });

    // --- Events Tactiles ---
    tinderContainer.addEventListener("touchstart", (e) => {
        currentCard = getTopCard();
        if (!currentCard) return;
        isDragging = true;
        startX = e.touches[0].clientX;
        currentCard.style.transition = "none";
    });

    tinderContainer.addEventListener("touchmove", (e) => {
        if (!isDragging || !currentCard) return;
        const deltaX = e.touches[0].clientX - startX;
        currentCard.style.transform = `translateX(${deltaX}px) rotate(${deltaX/10}deg)`;
    });0

    tinderContainer.addEventListener("touchend", (e) => {
        if(!isDragging || !currentCard) return;
        const deltaX = e.changedTouches[0].clientX - startX;
        handleSwipe(deltaX);
        isDragging = false;
    });

    function handleSwipe(deltaX) {
        const sensitivity = 80; 
        if(Math.abs(deltaX) > sensitivity){
            const direction = deltaX > 0 ? 'like' : 'dislike'; 
            currentCard.style.transition = "transform 0.4s ease-out, opacity 0.4s ease-out";
            currentCard.style.transform = `translateX(${deltaX > 0 ? 1000 : -1000}px) rotate(${deltaX > 0 ? 45 : -45}deg)`;
            currentCard.style.opacity = 0;
            const clientId = currentCard.dataset.clientId; 
            sendSwipe(clientId, direction);
            setTimeout(()=>{
                currentCard.remove();
                const nextCard = getTopCard();
                if (nextCard) {
                    nextCard.style.transition = 'transform 0.3s ease'; 
                    nextCard.style.transform = 'scale(1)'; 
                }
                currentCard = null; 
            }, 400);
        } else {
            currentCard.style.transition = "transform 0.3s ease";
            currentCard.style.transform = "translateX(0) rotate(0)";
            currentCard = null; 
        }
    }
    function sendSwipe(clientId, action) {
        fetch('/save_swipe', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ client_id: clientId, action: action })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Swipe enregistré", data);
            // Si c'est un like, on recharge la page pour voir le tableau se remplir !
            if (action === 'like' && data.status === 'success') {
                setTimeout(() => location.reload(), 500);
            }
        })
        .catch(err => console.error("Erreur swipe", err));
    }
}

document.addEventListener('DOMContentLoaded', function() {
    
    // --- Logique pour la recherche d'intervenant ---
    
    const searchForm = document.getElementById("searchForm");

    // On vérifie si le formulaire existe sur la page actuelle avant de continuer
    if (searchForm) {

        // Fonction utilitaire (interne à ce bloc)
        function normalizeTextJS(text) {
            if (!text) return '';
            return text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
        }

        searchForm.addEventListener("submit", function(e) {
            e.preventDefault(); // On bloque l'envoi classique
            
            const nom_input = this.nom.value.trim();
            const prenom_input = this.prenom.value.trim();

            const nom_url = normalizeTextJS(nom_input);
            const prenom_url = normalizeTextJS(prenom_input);

            if(nom_url && prenom_url){
                // Redirection vers la route Flask
                window.location.href = `/Intervenants/${encodeURIComponent(nom_url)}.${encodeURIComponent(prenom_url)}`;
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    
    // --- Logique pour la recherche de Client ---
    
    // Assurez-vous que l'ID du formulaire dans clients.html est bien "searchForm"
    const searchFormClient = document.getElementById("searchFormClient"); 

    // On vérifie si le formulaire existe sur la page actuelle avant de continuer
    if (searchFormClient) {

        // Fonction utilitaire (interne à ce bloc)
        function normalizeTextJS(text) {
            if (!text) return '';
            // Supprime les accents et met en minuscule pour une URL propre
            return text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
        }

        searchFormClient.addEventListener("submit", function(e) {
            e.preventDefault(); // On bloque l'envoi classique
            
            // On utilise 'this' (qui est le formulaire) pour accéder aux champs par leur attribut 'name'
            const nom_input = this.nom.value.trim();
            const prenom_input = this.prenom.value.trim();

            const nom_url = normalizeTextJS(nom_input);
            const prenom_url = normalizeTextJS(prenom_input);

            if(nom_url && prenom_url){
                // SEULE LIGNE MODIFIÉE on pointe vers /Clients/
                window.location.href = `/Clients/${encodeURIComponent(nom_url)}.${encodeURIComponent(prenom_url)}`;
            }
        });
    }
});


/* =========================================
   LOGIQUE AJOUT COMPETENCE (Protégée)
   ========================================= */
document.addEventListener('DOMContentLoaded', function() {
    const btnAddCompetence = document.getElementById('btn-add-competence');

    // On ne lance le code que si le bouton existe sur la page
    if (btnAddCompetence) {
        btnAddCompetence.addEventListener('click', function() {
            var container = document.getElementById('competences-container');
            var firstRow = container.getElementsByClassName('competence-row')[0];
            var newRow = firstRow.cloneNode(true);
            var inputs = newRow.getElementsByTagName('input');
            var selects = newRow.getElementsByTagName('select');
            
            if (inputs.length > 0) inputs[0].value = ''; 
            if (selects.length > 0) selects[0].selectedIndex = 0; 
            
            container.appendChild(newRow);
        });
    }
});

// La fonction supprimerLigne peut rester globale car elle est appelée via onclick="" dans le HTML
function supprimerLigne(btn) {
    var container = document.getElementById('competences-container');
    var rows = container.getElementsByClassName('competence-row');
    
    if (rows.length > 1) {
        btn.parentNode.remove();
    } else {
        alert("Vous devez avoir au moins une compétence.");
    }
}   


/* =========================================
   LOGIQUE RECHERCHE SECTEUR (Protégée)
   ========================================= */
document.addEventListener('DOMContentLoaded', function() {
    
    const formSecteur = document.getElementById('SearchFormSecteurClient');

    // On vérifie que le formulaire existe avant d'ajouter l'écouteur
    if (formSecteur) {
        formSecteur.addEventListener('submit', function(event) {
            event.preventDefault(); // Empêche le rechargement
            console.log("Formulaire secteur soumis via JS !"); // Debug

            const secteurInput = document.getElementById('secteur-input');
            if (secteurInput) {
                const secteur = secteurInput.value.trim();
                if (secteur) {
                    fetchClientProfiles(secteur);
                }
            }
        });
    }
});

// Ces fonctions peuvent rester en dehors car ce sont des définitions, pas des exécutions
function fetchClientProfiles(secteur) {
    const encodedSecteur = encodeURIComponent(secteur);
    const url = `/api/recherche/clients?secteur=${encodedSecteur}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            afficherResultats(data.profils);
        })
        .catch(error => {
            console.error('Erreur lors de la recherche :', error);
            const container = document.getElementById('resultats-secteur');
            if(container) container.innerHTML = `<p class="error">Erreur serveur : ${error.message}</p>`;
        });
}

function afficherResultats(profils) {
    const container = document.getElementById('resultats-secteur');
    if (!container) return; // Sécurité
    
    container.innerHTML = ''; 
    
    if (profils.length === 0) {
        container.innerHTML = '<p>Aucun client trouvé pour ce secteur d\'activité.</p>';
        return;
    }

    const ul = document.createElement('ul');
    profils.forEach(link => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        
        // Nettoyage pour obtenir le nom affichable
        const parts = link.split('/');
        const nom_lien = parts[parts.length - 1]; // ex: dupont.jean
    
        a.href = link; 
        a.textContent = nom_lien.replace('.', ' '); // Optionnel : rend le texte plus joli (DUPONT JEAN)
        a.target = "_blank";
        
        li.appendChild(a);
        ul.appendChild(li);
    });
    container.appendChild(ul);
}

