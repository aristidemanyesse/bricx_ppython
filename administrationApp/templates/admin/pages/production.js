

$(function(){

    $(".formExigence").submit(function(event) {
        Loader.start();
        var url = "/administration/organisation/ajax/exigence/";
        var formdata = new FormData($(this)[0]);
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