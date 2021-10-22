$(function () {

    //nouvelle commande
    $("body").on("click", "button.newproduit", function (event) {
        var url = "../../commandes/ajax_new_commande/new_produit/";
        var id = $(this).attr("data-id");
        var zone = $("select[name=zone]").val();
        $.post(url, { id: id, zone: zone }, (data) => {
            $("tbody.new_commande").append(data);
            $("button[data-id =" + id + "]").hide(200);
            actualise()
        }, "html");
    });


    delete_ligne = function (id) {
        var url = "../../commandes/ajax_new_commande/delete_ligne/";
        $.post(url, { id: id }, (data) => {
            $("tbody.new_commande tr[data-id =" + id + "]").hide(400).remove();
            $("button[data-id =" + id + "]").show(200);
            actualise()
        });
    }



    actualise = function () {
        var url = "../../commandes/ajax_new_commande/actualise/";
        var formdata = new FormData($("#formCommande")[0]);
        var tableau = new Array();
        $("#modal-newcommande .new_commande tr").each(function (index, el) {
            var id = $(this).attr('data-id');
            var val = $(this).find('input').val();
            var item = id + "=" + val;
            tableau.push(item);
        });
        var zone = $("#modal-newcommande select[name=zone]").val();
        formdata.append('tableau', tableau);
        formdata.append('zone', zone);
        $.post({ url: url, data: formdata, contentType: false, processData: false }, function (data) {
            $("#modal-newcommande tbody.new_commande").html(data);

            $.post({ url: "../../commandes/ajax_new_commande/total/", data: formdata, contentType: false, processData: false }, function (data) {
                $("#modal-newcommande .tva").html(data.tva);
                $("#modal-newcommande .montant").html(data.montant);
                $("#modal-newcommande .avance").html(data.avance);
                $("#modal-newcommande .total").html(data.total);
            }, 'json')
        }, 'html')
        return formdata;
    }



    $("body").on("change", "#modal-newcommande input, select[name=zone]", function () {
        actualise();
    })



    valider_commande = function () {
        var formdata = new FormData($("#formCommande")[0]);
        tableau = new Array();
        $("#modal-newcommande .new_commande tr").each(function (index, el) {
            var id = $(this).attr('data-id');
            var val = $(this).find('input').val();
            var item = id + "=" + val;
            tableau.push(item);
        });
        formdata.append('listeproduits', tableau);

        alerty.confirm("Voulez-vous vraiment valider la commande ?", {
            title: "Validation de la commande",
            cancelLabel: "Non",
            okLabel: "OUI, valider",
        }, function () {
            Loader.start();
            var url = "../../commandes/ajax_new_commande/valider_commande/";
            $.post({ url: url, data: formdata, contentType: false, processData: false }, function (data) {
                if (data.status) {
                    window.open(data.url, "_blank");
                    window.location.reload();
                    window.open(data.url1, "_blank");
                } else {
                    Alerter.error('Erreur !', data.message);
                }
            }, 'json')
        })
    }


    $(".formReglerCommande").submit(function (event) {
        $this = $(this);
        var url = "../../commandes/ajax_new_commande/regler_commande/";
        alerty.confirm("Voulez-vous vraiment valider le payement ?", {
            title: "Recouvrement de la commande",
            cancelLabel: "Non",
            okLabel: "OUI, valider",
        }, function () {
            var formdata = new FormData($this[0]);
            Loader.start();
            $.post({ url: url, data: formdata, contentType: false, processData: false }, function (data) {
                if (data.status) {
                    window.open(data.url, "_blank");
                    window.location.reload();
                } else {
                    Alerter.error('Erreur !', data.message);
                }
            }, 'json')
        })
        return false;
    });
    
    

    
    $(".formChangement").submit(function (event) {
        var tableau = new Array();
        $(this).parents(".modal").find("tbody tr").each(function (index, el) {
            var id = $(this).attr('data-id');
            var val = $(this).find('input').val();
            var item = id + "=" + val;
            tableau.push(item);
        });
        var formdata = new FormData($(this)[0]);
        formdata.append('tableau', tableau);
        alerty.confirm("Voulez-vous vraiment confirmer la changement de ces produits ?", {
            title: "Changement de produits",
            cancelLabel: "Non",
            okLabel: "OUI, changer",
        }, function () {
            Loader.start();
            var url = "../../commandes/ajax_new_commande/changer_produit/";
            $.post({ url: url, data: formdata, contentType: false, processData: false }, function (data) {
                if (data.status) {
                    window.location.reload();
                } else {
                    Alerter.error('Erreur !', data.message);
                }
            }, 'json')
        })
        return false;
    });

})