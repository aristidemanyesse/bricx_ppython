$(function(){

    $(".formPrix").submit(function(event) {
        Loader.start();
        var url = "/administration/organisation/ajax/price/";
        var formdata = new FormData($(this)[0]);
        var tableau = new Array();
        $(this).find("input[data-id]").each(function(configuration, el) {
            var id = $(this).attr('data-id');
            var val = $(this).val();
            var item = id+"="+val;
            tableau.push(item);
        });
        formdata.append('tableau', tableau);
        $.post({url:url, data:formdata, contentType:false, processData:false}, function(data){
            if (data.status) {
                window.location.reload();
            }else{
                Alerter.error('Erreur !', data.message);
            }
        }, 'json')
        return false;
    });



    $("form.formPayeProduit").submit(function(event) {
        Loader.start();
        var url = "/administration/organisation/ajax/paye_produit/";
        var formdata = new FormData($(this)[0]);
        var tableau = new Array();
        $(this).find("input[data-id][name=price]").each(function(configuration, el) {
            var id = $(this).attr('data-id');
            var val = $(this).val();
            var item = id+"="+val;
            tableau.push(item);
        });

        var tableau1= new Array();
        $(this).find("input[data-id][name=price_rangement]").each(function(configuration, el) {
            var id = $(this).attr('data-id');
            var val = $(this).val();
            var item = id+"="+val;
            tableau1.push(item);
        });


        var tableau2= new Array();
        $(this).find("input[data-id][name=price_livraison]").each(function(configuration, el) {
            var id = $(this).attr('data-id');
            var val = $(this).val();
            var item = id+"="+val;
            tableau2.push(item);
        });

        formdata.append('tableau', tableau);
        formdata.append('tableau1', tableau1);
        formdata.append('tableau2', tableau2);
        $.post({url:url, data:formdata, contentType:false, processData:false}, function(data){
            if (data.status) {
                window.location.reload();
            }else{
                Alerter.error('Erreur !', data.message);
            }
        }, 'json')
        return false;
    });



    $("form.formPayeProduitFerie").submit(function(event) {
        Loader.start();
        var url = "/administration/organisation/ajax/paye_produit_ferie/";
        var formdata = new FormData($(this)[0]);
        var tableau = new Array();
        $(this).find("input[data-id][name=price]").each(function(configuration, el) {
            var id = $(this).attr('data-id');
            var val = $(this).val();
            var item = id+"="+val;
            tableau.push(item);
        });

        var tableau1= new Array();
        $(this).find("input[data-id][name=price_rangement]").each(function(configuration, el) {
            var id = $(this).attr('data-id');
            var val = $(this).val();
            var item = id+"="+val;
            tableau1.push(item);
        });


        var tableau2= new Array();
        $(this).find("input[data-id][name=price_livraison]").each(function(configuration, el) {
            var id = $(this).attr('data-id');
            var val = $(this).val();
            var item = id+"="+val;
            tableau2.push(item);
        });

        formdata.append('tableau', tableau);
        formdata.append('tableau1', tableau1);
        formdata.append('tableau2', tableau2);
        $.post({url:url, data:formdata, contentType:false, processData:false}, function(data){
            if (data.status) {
                window.location.reload();
            }else{
                Alerter.error('Erreur !', data.message);
            }
        }, 'json')
        return false;
    });



})