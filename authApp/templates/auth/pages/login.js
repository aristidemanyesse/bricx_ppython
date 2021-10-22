$(function(){

    $("form#formConnexion").submit(function(event) {
        Loader.start();
        var url = "../ajax/login/";
        var formData = new FormData($(this)[0]);
        $.post({ url: url, data: formData, processData: false, contentType: false}, function(data){
            if (data.status) {
                if (data.new) {
                    Loader.stop();
                    localStorage.setItem("user_id", data.user_id)
                    $("#modal-newUser").modal();
                }else{
                    window.location.href = "/home/";
                }
            }else{
                Alerter.error('Erreur !', data.message);
            }
        });
        return false;
    });



    $("form#formNewUser").submit(function(event) {
        Loader.start();
        var url = "../ajax/first_user/";
        var formData = new FormData($(this)[0]);

        $.post({url: url, data: formData, processData: false, contentType: false}, function(data){
            if (data.status) {
                window.location.href = "/home/";
            }else{
                Alerter.error('Erreur !', data.message);
            }
        });
        return false;
    });


})