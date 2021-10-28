$(function () {

    $("body").on("click", "button.newressource", function (event) {
        var url = "/fabrique/appros/ajax/new_ressource/";
        var id = $(this).attr("data-id");
        $.post(url, { action: "newressource", id: id }, (data) => {
            $("tbody.approvisionnement").append(data);
            $("button[data-id =" + id + "]").hide(200);
            actualise()
        }, "html");
    });



    delete_ligne = function (id) {
        var url = "/fabrique/appros/ajax/delete_ligne/";
        $.post(url, { id: id }, (data) => {
            $("tbody.approvisionnement tr[data-id =" + id + "]").hide(400).remove();
            $("button[data-id =" + id + "]").show(200);
            actualise()
        });
    }


    actualise = function () {
        var url = "/fabrique/appros/ajax/actualise/";
        var formdata = new FormData($("#formApprovisionnement")[0]);
        var tableau = new Array();
        $("#modal-approvisionnement .approvisionnement tr, #modal-approvisionnement_ .approvisionnement tr").each(function (index, el) {
            var id = $(this).attr('data-id');
            var qte = $(this).find('input[name=quantite]').val();
            var prix = $(this).find('input[name=prix]').val();
            var item = id + "=" + qte + "=" + prix;
            tableau.push(item);
        });
        formdata.append('tableau', tableau);
        $.post({ url: url, data: formdata, contentType: false, processData: false }, function (data) {

            url = "/fabrique/appros/ajax/total/";
            $.post({ url: url, data: formdata, contentType: false, processData: false }, function (data) {
                $(".montant").html(data.montant);
                $(".avance").html(data.avance);
                $(".total").html(data.total);
                total = data.total;
            }, 'json')
        }, 'html')
        return formdata;
    }


    $("body").on("change", "#modal-approvisionnement input, #modal-approvisionnement select", function () {
        actualise();
    })


    validerApprovisionnement = function () {
        formdata = actualise();
        alerty.confirm("Voulez-vous vraiment confirmer cet approvisionnement ?", {
            title: "Validation de l'approvisionnement",
            cancelLabel: "Non",
            okLabel: "OUI, confirmer",
        }, function () {
            if (parseInt(total) == 0) {
                alerty.confirm("Le montant total de cet approvisionnement est de 0F ! Est-il vraiment exact?", {
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
        url = "/fabrique/appros/ajax/valider_approvisionnement/";
        $.post({ url: url, data: formdata, contentType: false, processData: false }, function (data) {
            if (data.status) {
                window.open(data.url, "_blank");
                window.location.reload();
            } else {
                Alerter.error('Erreur !', data.message);
            }
        }, 'json')
    }



    $(".formValiderApprovisionnement").submit(function(event) {
        Loader.start();
        url = "/fabrique/appros/ajax/terminer_appro/";
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




    $(".formReglerAppro").submit(function (event) {
        $this = $(this);
        url = "/fabrique/appros/ajax/regler_appro/";
        alerty.confirm("Voulez-vous vraiment valider le payement ?", {
            title: "Recouvrement de l'approvisionnemnt",
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