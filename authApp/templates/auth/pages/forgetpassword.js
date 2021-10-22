

$(function(){


    $("form#resetForm").submit(function(event) {
        Loader.start();
        var url = "../ajax/forgetpassword/";
        var formData = new FormData($(this)[0]);
        $.post({url:url, data:formData, processData:false, contentType:false}, function(data) {
            if (data.status) {
                alerty.confirm("Nous vous avons envoyé un mail pour confirmer le chagement de votre mot de paasse. \n Consulter le mail pour poursuivre la procédure ! ", {
                    title: "En attente de confirmation",
                    cancelLabel : ".",
                    okLabel : "Ok",
                }, function(){
                    window.location.href = data.url;
                }, function(){
                    window.location.href = data.url;
                });
            }else{
                Alerter.error('Erreur !', data.message);
            }
        }, 'json');
        return false;
    });

})