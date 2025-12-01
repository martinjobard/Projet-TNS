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