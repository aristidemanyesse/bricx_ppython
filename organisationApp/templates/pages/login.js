$(function(){

    $("form#formConnexion").submit(function(event) {
        Loader.start();
        var url = "http://localhost:8000/auth/traitement/login";
        var formData = new FormData($(this)[0]);
        $.post({url:url, data:formData, processData:false, contentType:false}, function(data) {
            if (data.status) {
                if (data.new) {
                    Loader.stop();
                    $("#modal-newUser").modal();
                }else{
                    window.location.href = data.url;
                }
            }else{
            Alerter.error('Erreur !', data.message);
            }
        }, 'json');
        return false;
    });



    $("form#formNewUser").submit(function(event) {
        Loader.start();
        var url = "http://localhost:8000/auth/traitement/first_user";
        var formData = new FormData($(this)[0]);
        $.post({url:url, data:formData, processData:false, contentType:false}, function(data) {
            if (data.status) {
                window.location.href = data.url;
            }else{
            Alerter.error('Erreur !', data.message);
            }
        }, 'json');
        return false;
    });


})