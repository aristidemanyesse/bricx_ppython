$(function () {

    $("body").on("click", "button.newproduit", function (event) {
        var url = "/fabrique/appros/ajax_achatstock/new_produit/";
        var id = $(this).attr("data-id");
        $.post(url, { action: "newproduit", id: id }, (data) => {
            $("tbody.achatstock").append(data);
            $("button[data-id =" + id + "]").hide(200);
            actualise()
        }, "html");
    });



    delete_ligne = function (id) {
        var url = "/fabrique/appros/ajax_achatstock/delete_ligne/";
        $.post(url, { id: id }, (data) => {
            $("tbody.achatstock tr[data-id =" + id + "]").hide(400).remove();
            $("button[data-id =" + id + "]").show(200);
            actualise()
        });
    }


    actualise = function () {
        var url = "/fabrique/appros/ajax_achatstock/actualise/";
        var formdata = new FormData($("#formAchat")[0]);
        var tableau = new Array();
        $("#modal-achatstock .achatstock tr, #modal-achatstock_ .achatstock tr").each(function (index, el) {
            var id = $(this).attr('data-id');
            var qte = $(this).find('input[name=quantite]').val();
            var prix = $(this).find('input[name=prix]').val();
            var item = id + "=" + qte + "=" + prix;
            tableau.push(item);
        });
        formdata.append('tableau', tableau);
        $.post({ url: url, data: formdata, contentType: false, processData: false }, function (data) {

            url = "/fabrique/appros/ajax_achatstock/total/";
            $.post({ url: url, data: formdata, contentType: false, processData: false }, function (data) {
                $(".montant").html(data.montant);
                $(".avance").html(data.avance);
                $(".total").html(data.total);
                montant = data.montant;
                total = data.total;
            }, 'json')
        }, 'html')
        return formdata;
    }


    $("body").on("change", "#modal-achatstock input, #modal-achatstock select", function () {
        actualise();
    })


    validerAchatStock = function () {
        formdata = actualise();
        alerty.confirm("Voulez-vous vraiment confirmer cet achat de briques ?", {
            title: "Validation de l'achat de briques",
            cancelLabel: "Non",
            okLabel: "OUI, confirmer",
        }, function () {
            if (parseInt(montant) == 0) {
                alerty.confirm("Le montant total de cet achat de briques est de 0F ! Est-il vraiment exact?", {
                    title: "Attention",
                    cancelLabel: "Non",
                    okLabel: "OUI, confirmer",
                }, function () {
                    valider(formdata)
                })
            } else {
                valider(formdata)
            }

        })
    }


    valider = function (formdata) {
        Loader.start();
        url = "/fabrique/appros/ajax_achatstock/valider_achatstock/";
        $.post({ url: url, data: formdata, contentType: false, processData: false }, function (data) {
            if (data.status) {
                window.open(data.url, "_blank");
                window.location.reload();
            } else {
                Alerter.error('Erreur !', data.message);
            }
        }, 'json')
    }



    $(".formValiderAchatStock").submit(function(event) {
        Loader.start();
        url = "/fabrique/appros/ajax_achatstock/terminer_achat/";
        var formdata = new FormData($(this)[0]);
        var tableau = new Array();
        $(this).find("table tr").each(function(index, el) {
         var id = $(this).attr('data-id');
         var val = $(this).find('input').val();
         var item = id+"="+val;
         tableau.push(item);
     });
        formdata.append('tableau', tableau);
        $.post({url:url, data:formdata, contentType:false, processData:false}, function(data){
         if (data.status) {
             window.location.reload()
         }else{
             Alerter.error('Erreur !', data.message);
         }
     }, 'json');
        return false;
    });




    $(".formReglerAchatStock").submit(function (event) {
        $this = $(this);
        url = "/fabrique/appros/ajax_achatstock/regler_achat/";
        alerty.confirm("Voulez-vous vraiment valider le payement ?", {
            title: "Recouvrement de l'achat de stock",
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
    
    
})