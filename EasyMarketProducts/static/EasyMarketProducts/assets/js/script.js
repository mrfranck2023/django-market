// document.addEventListener("DOMContentLoaded", function () {
//     // Sélectionne tous les champs de quantité
//     const quantites = document.querySelectorAll(".quantite");

//     function calculerMontant() {
//         let total = 0;

//         quantites.forEach(input => {
//             const prixUnitaire = parseFloat(input.dataset.price); // Récupère le prix unitaire depuis data-price
//             const quantite = parseInt(input.value) || 0; // Quantité saisie (0 si vide)
//             const montantTTC = prixUnitaire * quantite; // Calcul du montant

//             // Mettre à jour la colonne "Montant TTC"
//             const montantCell = input.closest("tr").querySelector(".montant-ttc");
//             montantCell.textContent = montantTTC.toFixed(2); // Affichage avec 2 décimales

//             // Ajouter au total général
//             total += montantTTC;
//         });

//         // Mettre à jour le "Net à payer"
//         document.getElementById("net-a-payer").textContent = total.toFixed(2);
//     }

//     // Ajoute un écouteur sur chaque input quantité
//     quantites.forEach(input => {
//         input.addEventListener("input", calculerMontant);
//     });

//     // Exécuter une première fois pour initialiser le total
//     calculerMontant();
// });


// const socket = new WebSocket("ws://127.0.0.1:8000/ws/socket-server/");

// socket.onopen = function(event) {
//     console.log("Connexion WebSocket établie !");
// };

// socket.onmessage = function(event) {
//     const data = JSON.parse(event.data);
//     console.log("Données reçues :", data);

//     // Rafraîchir dynamiquement la liste des produits dans le tableau
//     if (data.barcode) {
//         fetch("/easyMarketProducts/caissier-index/")  // Appelle ta vue Django qui retourne la liste mise à jour
//             .then(response => response.text())
//             .then(html => {
//                 document.getElementById("produits-liste").innerHTML = html;
//             });
//     }
// };

// socket.onclose = function(event) {
//     console.log("Connexion WebSocket fermée.");
// };
const socket = new WebSocket("ws://127.0.0.1:8000/ws/socket-server/");

socket.onopen = function(event) {
    console.log("Connexion WebSocket établie !");
};

socket.onmessage = function(event) {
    console.log("Données reçues :", data);
    const data = JSON.parse(event.data);
    console.log("je suis data et ceci ce sont mes données", data);

    if (data.error) {
        alert(data.error);
    } else {
        addProductToTable(data);
    }
};

socket.onclose = function(event) {
    console.log("Connexion WebSocket fermée.");
};

// Fonction pour ajouter un produit au tableau HTML
function addProductToTable(product) {
    const tableBody = document.getElementById("produits-liste");
    
    // Vérifier si le produit est déjà dans le tableau (évite les doublons)
    if (document.getElementById(`product-${product.id}`)) {
        return;
    }
    const newRow = document.createElement("tr");
    newRow.id = `product-${product.id}`;
    newRow.innerHTML = `
        <th scope="row">${product.id}</th>
        <td>${product.name}</td>
        <td><input type="number" class="quantite" min="1" value="1" data-price="${product.price}"></td>
        <td class="pu-ttc">${product.price.toFixed(2)}</td>
        <td class="montant-ttc">${product.price.toFixed(2)}</td>
    `;
    tableBody.appendChild(newRow);
}
