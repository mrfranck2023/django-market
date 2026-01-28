function updateTotal() {
    let total = 0;
    $('.montant-ttc').each(function() {
        total += parseFloat($(this).text());
    });
    $('#net-a-payer strong').text(total.toFixed(2) + "€");
}

// Mettre à jour le montant TTC lorsqu'on change la quantité
$(document).on('input', '.quantite', function() {
    const $row = $(this).closest('tr');
    const quantite = parseInt($(this).val());
    const price = parseFloat($(this).data('price'));
    const montantTTC = quantite * price;
    $row.find('.montant-ttc').text(montantTTC.toFixed(2));
    updateTotal();
});

$(document).ready(function() {
    const $addBtn = $("#add-product");
    const $produitsListe = $("#produits-liste");
    const $template = $("#template-produit");
    const $netAPayerEl = $("#net-a-payer");
        
    // Ajouter un produit
    $addBtn.on("click", function() {
        const $clone = $template.clone();
        $clone.removeClass("d-none").removeAttr("id");
        $produitsListe.append($clone);
        updateMontants();
    });

    // Supprimer un produit
    $produitsListe.on("click", ".remove-btn", function() {
        $(this).closest("tr").remove();
        updateMontants();
    });

    // Recalcul automatique quand quantité ou prix change
    $produitsListe.on("input", ".quantite, .prix", function() {
        updateMontants();
    });

    const socket = new WebSocket("ws://127.0.0.1:8000/ws/socket-server/");

    socket.onopen = function(event) {
        console.log("Connexion WebSocket établie !");
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log("je suis data et ceci ce sont mes données", data);

        if (data.error) {
            alert(data.error);
        } else {
            addProductToTable(data.product);
        }
    };

    socket.onclose = function(event) {
        console.log("Connexion Web3 Socket fermée.");
    };

    // Fonction pour ajouter un produit au tableau HTML
    function addProductToTable(product) {
        // Vérifier si le produit est déjà dans le tableau (évite les doublons)
    if ($(`#product-${product.id}`).length) {

        const $row = $(`#product-${product.id}`);

        const $qteInput = $row.find(".quantite");

        let qte = parseInt($qteInput.val()) || 0;

        qte += 1;

        $qteInput.val(qte);

        const price = parseFloat($qteInput.attr("data-price"));

        const montant = qte * price;

        $row.find(".montant-ttc").text(montant.toFixed(2));

        updateMontants(); // recalcul total général

        console.log("Quantité incrémentée :", qte);

        // 🎯 Effet visuel rapide
        $row.addClass("table-success");
        setTimeout(() => {
            $row.removeClass("table-success");
        }, 300);


        return;
    }

        const $produitsListe = $("#produits-liste");
        const $template = $("#template-produit");
        const $clone = $template.clone();
        $clone
        .removeClass("d-none")
        .removeAttr("id")
        .attr("id", `product-${product.id}`);

        // Remplir les champs du template
        $clone.find('input[name="ref[]"]').val(product.id);
        $clone.find('input[name="designation[]"]').val(product.name);
        $clone.find('.quantite').val(1).attr("data-price", product.price);
        $clone.find('.montant-ttc').text(product.price.toFixed(2));

        // Si tu as un champ prix dans le template
        $clone.find('.prix').val(product.price);

        $produitsListe.append($clone);

        updateMontants();
    }

    function updateMontants() {
        let total = 0;
        $produitsListe.find("tr").not(".d-none").each(function() {
            const $row = $(this);
            const qte = parseFloat($row.find(".quantite").val()) || 0;
            const prix = parseFloat($row.find(".prix").val()) || 0;
            const montant = qte * prix;
        
            $row.find(".montant-ttc").text(montant.toFixed(2));
            total += montant;
        });
        $netAPayerEl.text(total.toFixed(2));
    }
});
