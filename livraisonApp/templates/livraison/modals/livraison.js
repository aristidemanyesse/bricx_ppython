$(function () {

    $(".formLivraison").submit(function (event) {
        var formdata = new FormData($(this)[0]);
        var tableau = new Array();
        $(this).parents(".modal").find(".livraison tr").each(function (index, el) {
            var id = $(this).attr('data-id');
            var livree = $(this).find('input[name=livree]').val();
            var surplus = $(this).find('input[name=surplus]').val();
            var perte = $(this).find('input[name=perte]').val();
            var item = id + "=" + livree + "=" + surplus + "=" + perte;
            tableau.push(item);
        });
        formdata.append('listeproduits', tableau);

        alerty.confirm("Voulez-vous vraiment confirmer la livraison de ces produits ?", {
            title: "livraison de la commande",
            cancelLabel: "Non",
            okLabel: "OUI, livrer",
        }, function () {
            Loader.start();
            var url = "../../livraison/ajax/livraison/";
            $.post({ url: url, data: formdata, contentType: false, processData: false }, function (data) {
                if (data.status) {
                    window.open(data.url, "_blank");
                    window.location.reload();
                } else {
                    Alerter.error('Erreur !', data.message);
                }
            }, 'json')
        })
    });

});