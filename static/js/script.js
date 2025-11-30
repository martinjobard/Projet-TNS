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