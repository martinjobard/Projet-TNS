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

    const cardColors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#FFA500", "#800080", "#D3D3D3", "#000000"];

    function createCards() {
        for(let i = 0; i < cardColors.length; i++){
            const card = document.createElement("div");
            card.className = "card";
            card.style.backgroundColor = cardColors[i];
            const cardContent = document.createElement("div"); 
            cardContent.className = "card-content";
            cardContent.textContent = (i + 1).toString();
            card.appendChild(cardContent);
            tinderContainer.appendChild(card);
        }
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
    });

    tinderContainer.addEventListener("touchend", (e) => {
        if(!isDragging || !currentCard) return;
        const deltaX = e.changedTouches[0].clientX - startX;
        handleSwipe(deltaX);
        isDragging = false;
    });

    function handleSwipe(deltaX) {
        const sensitivity = 80; 
        if(Math.abs(deltaX) > sensitivity){
            currentCard.style.transition = "transform 0.4s ease-out, opacity 0.4s ease-out";
            currentCard.style.transform = `translateX(${deltaX > 0 ? 1000 : -1000}px) rotate(${deltaX > 0 ? 45 : -45}deg)`;
            currentCard.style.opacity = 0;
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