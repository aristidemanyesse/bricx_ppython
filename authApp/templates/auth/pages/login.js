$(function(){

    $("form#formConnexion").submit(function(event) {
        Loader.start();
        var url = "http://127.0.0.1:9000/auth/ajax/login/";
        var formData = new FormData($(this)[0]);

        $.ajax({
            url: url,
            data: formData,
            processData: false,
            contentType: false,
            type: 'POST',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
            xhrFields: {
                withCredentials: true
            },
            success: function(data){
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
            }
        });
        return false;
    });



    $("form#formNewUser").submit(function(event) {
        Loader.start();
        var url = "http://127.0.0.1:9000/auth/ajax/first_user/";
        var formData = new FormData($(this)[0]);

        $.ajax({
            url: url,
            data: formData,
            processData: false,
            contentType: false,
            type: 'POST',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
            xhrFields: {
                withCredentials: true
            },
            success: function(data){
                if (data.status) {
                    window.location.href = "/home/";
                }else{
                    Alerter.error('Erreur !', data.message);
                }
            }
        });


        return false;
    });


})