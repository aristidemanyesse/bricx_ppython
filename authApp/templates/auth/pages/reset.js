

$(function(){


    $("form#resetForm").submit(function(event) {
        Loader.start();
        var url = "../ajax/reset/";
        var formData = new FormData($(this)[0]);
        $.post({url:url, data:formData, processData:false, contentType:false}, function(data) {
            if (data.status) {
                alerty.confirm("Votre mot de passe a été changé avec succes. Vous allez être redirigé vers la page de connexion ! ", {
                    title: "Mot de passe changé !",
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