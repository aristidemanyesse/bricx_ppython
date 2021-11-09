$(function () {

    $("#FormEntree, #FormDepense").submit(function (event) {
        $this = $(this);
        var url = "/tresorerie/ajax/operation/";
        alerty.confirm("Voulez-vous vraiment valider cette opération ?", {
            title: "Nouvelle opération de caisse",
            cancelLabel: "Non",
            okLabel: "OUI, valider",
        }, function () {
            var formdata = new FormData($this[0]);
            Loader.start();
            $.post({ url: url, data: formdata, contentType: false, processData: false }, function (data) {
                if (data.status) {
                    window.open(data.url, "_blank");
                    window.location.reload();
                } else {
                    Alerter.error('Erreur !', data.message);
                }
            }, 'json')
        })
        return false;
    });


    $("#FormTransfert").submit(function (event) {
        $this = $(this);
        var url = "/tresorerie/ajax/transfert/";
        alerty.confirm("Voulez-vous vraiment valider ce transfert ?", {
            title: "Nouveau transfert de fond",
            cancelLabel: "Non",
            okLabel: "OUI, valider",
        }, function () {
            alerty.prompt("Entrer votre mot de passe pour confirmer l'opération !", {
                title: 'Récupération du mot de passe !',
                inputType: "password",
                cancelLabel: "Annuler",
                okLabel: "Valider"
            }, function (password) {
                var formdata = new FormData($("#FormTransfert")[0]);
                formdata.append('password', password);
                Loader.start();
                $.post({ url: url, data: formdata, contentType: false, processData: false }, function (data) {
                    if (data.status) {
                        window.location.reload();
                    } else {
                        Alerter.error('Erreur !', data.message);
                    }
                }, 'json')
            })
        })
        return false;
    });




    valider_mouvement = function(id){
        var url = "/tresorerie/ajax/valider_mouvement/";
		alerty.confirm("Confirmez-vous être maintenant en possession effective de ladite somme ?", {
			title: "Validation de l'opération",
			cancelLabel : "Non",
			okLabel : "OUI, valider",
		}, function(){
			alerty.prompt("Entrer votre mot de passe pour confirmer l'opération !", {
				title: 'Récupération du mot de passe !',
				inputType : "password",
				cancelLabel : "Annuler",
				okLabel : "Valider"
			}, function(password){
				Loader.start();
				$.post(url, {action:"valider", password:password, id:id}, (data)=>{
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

