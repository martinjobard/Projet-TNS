// static/js/script.js

function toggleSousMenu(e) {
    // 1. Empêche le lien de recharger la page
    e.preventDefault();
    
    // 2. Sélectionne le sous-menu qui suit juste après le lien cliqué
    var sousMenu = e.target.nextElementSibling;
    
    // 3. Ferme tous les autres sous-menus ouverts
    var tousLesSousMenus = document.querySelectorAll('.dropdown-content');
    tousLesSousMenus.forEach(function(menu) {
        if (menu !== sousMenu) {
            menu.classList.remove('afficher');
        }
    });

    // 4. Bascule l'affichage du menu cliqué
    sousMenu.classList.toggle("afficher");
}

// 5. Fermer le menu si on clique ailleurs sur la page
window.onclick = function(event) {
    // Si on ne clique PAS sur un bouton de menu (.dropbtn)
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            // Si un menu est ouvert, on le ferme
            if (openDropdown.classList.contains('afficher')) {
                openDropdown.classList.remove('afficher');
            }
        }
    }
}

function toggleSidebarItem(element) {
        // On empêche le lien de recharger la page
        event.preventDefault();
        
        // On sélectionne la liste <ul> qui suit juste après le lien cliqué
        var submenu = element.nextElementSibling;
        
        // On bascule l'affichage (Si caché -> affiche, Si affiché -> cache)
        if (submenu.style.display === "block") {
            submenu.style.display = "none";
        } else {
            submenu.style.display = "block";
        }
    }

/* --- GESTION DU MENU PROFIL --- */

function toggleProfileMenu() {
    // On cible le menu par son ID
    var menu = document.getElementById("monProfilDropdown");
    // On ajoute ou enlève la classe "active" (qui fait display: block)
    menu.classList.toggle("active");
}

// FERMETURE AUTOMATIQUE AU CLIC AILLEURS
window.onclick = function(event) {
    // Si on ne clique PAS sur l'avatar
    if (!event.target.matches('.avatar')) {
        var dropdowns = document.getElementsByClassName("profile-dropdown");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            // Si le menu est ouvert, on le ferme
            if (openDropdown.classList.contains('active')) {
                openDropdown.classList.remove('active');
            }
        }
    }
    
    // (Gardez ici votre code existant pour fermer les autres menus si vous en avez)
}

/* --- Page tinder-like --- */
const container = document.getElementById("card-container"); 
let isDragging = false;
let startX = 0;
let currentCard = null;

const cardColors = [
    "#FF0000",
    "#00FF00",
    "#0000FF",
    "#FFFF00",
    "#00FFFF",
    "#FF00FF",
    "#FFA500",
    "#800080",
    "#D3D3D3",
    "#000000"
];

// Boucle pour créer 10 cartes
function createCards() {
    for(let i = 0; i < cardColors.length; i++){
        const card = document.createElement("div");
        card.className = "card";
        card.style.backgroundColor = cardColors[i];
        
        // Création et ajout du contenu de la carte
        const cardContent = document.createElement("div"); 
        cardContent.className = "card-content";
        cardContent.textContent = (i + 1).toString();
        
        card.appendChild(cardContent);
        container.appendChild(card);
    }
}

// Nous appelons la fonction de création au démarrage du script
createCards();

// Fonction pour obtenir la carte du dessus
function getTopCard(){
    return container.querySelector(".card:last-child");
}


/* ------------------ Gestion des événements Souris ------------------ */

container.addEventListener("mousedown", (e) => {
    currentCard = getTopCard();
    if (!currentCard) return;
    isDragging = true;
    startX = e.clientX;
    currentCard.style.transition = "none"; // Désactiver les transitions pendant le drag
});

container.addEventListener("mousemove", (e) => {
    if(!isDragging || !currentCard) return;
    const deltaX = e.clientX - startX;
    currentCard.style.transform = `translateX(${deltaX}px) rotate(${deltaX/10}deg)`;
});

container.addEventListener("mouseup", (e) => {
    if(!isDragging || !currentCard) return;
    const deltaX = e.clientX - startX;
    handleSwipe(deltaX);
    isDragging = false;
});


/* ------------------ Gestion des événements Tactiles ------------------ */

container.addEventListener("touchstart", (e) => {
    currentCard = getTopCard();
    if (!currentCard) return;
    isDragging = true;
    startX = e.touches[0].clientX;
    currentCard.style.transition = "none";
});

container.addEventListener("touchmove", (e) => {
    if (!isDragging || !currentCard) return;
    const deltaX = e.touches[0].clientX - startX;
    currentCard.style.transform = `translateX(${deltaX}px) rotate(${deltaX/10}deg)`;
});

container.addEventListener("touchend", (e) => {
    if(!isDragging || !currentCard) return;
    const deltaX = e.changedTouches[0].clientX - startX;
    handleSwipe(deltaX);
    isDragging = false;
});


/* ------------------ Logique du Swipe ------------------ */

function handleSwipe(deltaX) {
    const sensitivity = 80; 
    
    if(Math.abs(deltaX) > sensitivity){
        // Swipe réussi: Éjecter la carte
        
        // La transition DOIT être la même durée que le setTimeout (0.4s = 400ms)
        currentCard.style.transition = "transform 0.4s ease-out, opacity 0.4s ease-out";
        
        // Déplacement rapide hors de l'écran et opacité à 0
        currentCard.style.transform = `translateX(${deltaX > 0 ? 1000 : -1000}px) rotate(${deltaX > 0 ? 45 : -45}deg)`;
        currentCard.style.opacity = 0;
        
        // La carte est supprimée seulement APRÈS la fin de l'animation (400ms)
        setTimeout(()=>{
            // 1. Suppression de la carte actuelle
            currentCard.remove();
            
            // 2. Récupération de la nouvelle carte du dessus
            const nextCard = getTopCard();
            if (nextCard) {
                // 3. Ré-activation de la transition pour la nouvelle carte
                nextCard.style.transition = 'transform 0.3s ease'; 
                // 4. Remise à l'échelle pour l'animation d'apparition
                nextCard.style.transform = 'scale(1)'; 
            }
            
            // currentCard doit rester null ICI, et être mis à jour au prochain mousedown/touchstart
            currentCard = null; 

        }, 400); // 400ms est la durée de l'animation.

    } else {
        // Swipe non réussi: Retour à la position initiale
        currentCard.style.transition = "transform 0.3s ease";
        currentCard.style.transform = "translateX(0) rotate(0)";
        
        // Après le retour, on annule la carte actuelle, elle est prête pour le prochain drag
        currentCard = null; 
    }
    
    // isDragging est déjà remis à false dans mouseup/touchend, donc pas besoin de le remettre ici
}

/*page mon compte*/
document.addEventListener('DOMContentLoaded', function() {
    // --- Boutons pour afficher/masquer les blocs ---
    const btnModifierProfil = document.getElementById('btn_modifier_profil'); // Pour Nom & Email
    const btnModifierMdp = document.getElementById('btn_modifier_mdp');     // Pour Mot de passe
    const btnModifierPdp = document.getElementById('btn_modifier_pdp');     // Pour Photo de profil (nouveau bouton)

    // --- Blocs de formulaires à afficher/masquer ---
    const blocNomEmail = document.getElementById('nom&email_modifier_block');
    const blocMdp = document.getElementById('mdp_modifier_block');
    const blocPdp = document.getElementById('pdp_modifier_block');

    // Fonction générique pour afficher un bloc et cacher les autres
    function toggleBlock(blockToShow) {
        // Cacher tous les blocs
        [blocNomEmail, blocMdp, blocPdp].forEach(block => {
            if (block) { // Vérifier si le bloc existe avant de tenter de le manipuler
                block.style.display = 'none';
            }
        });

        // Afficher le bloc désiré
        if (blockToShow && blockToShow.style.display === 'none') {
            blockToShow.style.display = 'block'; // Ou 'flex' si vous utilisez flexbox pour le layout
        } else if (blockToShow) {
            blockToShow.style.display = 'none'; // Si déjà affiché, le cacher
        }
    }

    // --- Écouteurs d'événements pour les boutons ---

    if (btnModifierProfil) {
        btnModifierProfil.addEventListener('click', function(event) {
            event.preventDefault(); // Empêche le comportement par défaut du lien/bouton
            toggleBlock(blocNomEmail);
        });
    }

    if (btnModifierMdp) {
        btnModifierMdp.addEventListener('click', function(event) {
            event.preventDefault();
            toggleBlock(blocMdp);
        });
    }

    if (btnModifierPdp) {
        btnModifierPdp.addEventListener('click', function(event) {
            event.preventDefault();
            toggleBlock(blocPdp);
        });
    }

});