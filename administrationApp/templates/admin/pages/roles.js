$(function(){


    lock = function(type, id){
        url = "../../composants/dist/shamman/traitement.php";
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
                $.post(url, {action:"lock", type:type, id:id, password:password}, (data)=>{
                    if (data.status) {
                        window.location.reload()
                    }else{
                        Alerter.error('Erreur !', data.message);
                    }
                },"json");
            })
        })
    }



    unlock = function(table, id){
        url = "../../composants/dist/shamman/traitement.php";
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
                $.post(url, {action:"unlock", table:table, id:id, password:password}, (data)=>{
                    if (data.status) {
                        window.location.reload()
                    }else{
                        Alerter.error('Erreur !', data.message);
                    }
                },"json");
            })
        })
    }



    resetPassword = function(table, id){
        url = "../../composants/dist/shamman/traitement.php";
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
                $.post(url, {action:"resetPassword", table:table, id:id, password:password}, (data)=>{
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