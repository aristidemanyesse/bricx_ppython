$(function(){

    $('input.i-checks').on('ifChanged', function(event){
        var url = "/administration/organisation/ajax/permissions/";
        var value = $(this).is(":checked");
        var employe_id = $(this).attr("employe_id");
        var perm_id = $(this).attr("perm_id");

        $.post(url, {value:value, employe_id:employe_id, perm_id:perm_id}, (data)=>{
            if (data.status) {
                Alerter.success('Reussite !', "Modification prise en compte avec succès !");
            }else{
                Alerter.error('Erreur !', data.message);
                return false;
            }
        },"json");
    });


    lock = function(id){
        var url = "/administration/organisation/ajax/lock/";
        alerty.confirm("Voulez-vous vraiment bloquer tout accès à cette personne ?", {
            title: "Restriction d'accès",
            cancelLabel : "Non",
            okLabel : "OUI, bloquer",
        }, function(){
            alerty.prompt("Entrer votre mot de passe pour confirmer l'opération !", {
                title: 'Récupération du mot de passe !',
                inputType : "password",
                cancelLabel : "Annuler",
                okLabel : "Valider"
            }, function(password){
                Loader.start();
                $.post(url, {id:id, password:password}, (data)=>{
                    if (data.status) {
                        window.location.reload()
                    }else{
                        Alerter.error('Erreur !', data.message);
                    }
                },"json");
            })
        })
    }



    unlock = function( id){
        var url = "/administration/organisation/ajax/unlock/";
        alerty.confirm("Vous êtes sur le point de redonner les accès à cette personne. Continuer ?", {
            title: "Restriction d'accès",
            cancelLabel : "Non",
            okLabel : "OUI, debloquer",
        }, function(){
            alerty.prompt("Entrer votre mot de passe pour confirmer l'opération !", {
                title: 'Récupération du mot de passe !',
                inputType : "password",
                cancelLabel : "Annuler",
                okLabel : "Mot de passe"
            }, function(password){
                Loader.start();
                $.post(url, { id:id, password:password}, (data)=>{
                    if (data.status) {
                        window.location.reload()
                    }else{
                        Alerter.error('Erreur !', data.message);
                    }
                },"json");
            })
        })
    }



    reset_password = function( id){
        var url = "/administration/organisation/ajax/reset_password/";
        alerty.confirm("Voulez-vous vraiment reinitialiser les accès de cette personne ?", {
            title: "Restriction d'accès",
            cancelLabel : "Non",
            okLabel : "OUI, reinitialiser",
        }, function(){
            alerty.prompt("Entrer votre mot de passe pour confirmer l'opération !", {
                title: 'Récupération du mot de passe !',
                inputType : "password",
                cancelLabel : "Annuler",
                okLabel : "Valider"
            }, function(password){
                Loader.start();
                $.post(url, { id:id, password:password}, (data)=>{
                    if (data.status) {
                        window.location.reload()
                    }else{
                        Alerter.error('Erreur !', data.message);
                    }
                },"json");
            })
        })
    }





})