$(function(){

	$("#formAcompte").submit(function(event) {
        url = "/fabrique/appros/ajax/crediter/";
		alerty.confirm("Voulez-vous vraiment créditer ce montant sur ce compte ?", {
			title: "Créditer l'acompte",
			cancelLabel : "Non",
			okLabel : "OUI, créditer",
		}, function(){
			var formdata = new FormData($("#formAcompte")[0]);
			Loader.start();
			$.post({url:url, data:formdata, contentType:false, processData:false}, function(data){
				if (data.status) {
					window.open(data.url, "_blank");
					window.location.reload();
				}else{
					Alerter.error('Erreur !', data.message);
				}
			}, 'json')
		})
		return false;
	});



	reglerToutesDettes = function(){
		alerty.confirm("Voulez-vous vraiment regler toutes les dettes de ce fournissseur ? \n Le Recouvrement se fera via le compte principal. veuillez donc vous assurer de son solde. \n Le recouvrement se fera également dans la limite des fonds disponibles", {
			title: "Recouvrement de dettes",
			cancelLabel : "Non",
			okLabel : "OUI, valider",
		}, function(){
            url = "/fabrique/appros/ajax/regler_toutes_dettes/";
			alerty.prompt("Entrer votre mot de passe pour confirmer l'opération !", {
				title: 'Récupération du mot de passe !',
				inputType : "password",
				cancelLabel : "Annuler",
				okLabel : "Valider"
			}, function(password){
				Loader.start();
				$.post(url, {password:password}, (data)=>{
					if (data.status) {
						window.location.reload()
					}else{
						Alerter.error('Erreur !', data.message);
					}
				},"json");
			})
		})
	}



	$("#formRembourser").submit(function(event) {
        url = "/fabrique/appros/ajax/rembourser/";
		alerty.confirm("Voulez-vous vraiment rembourser ce montant à ce client ?", {
			title: "rembourser l'acompte",
			cancelLabel : "Non",
			okLabel : "OUI, créditer",
		}, function(){
			var formdata = new FormData($("#formRembourser")[0]);
				Loader.start();
				$.post({url:url, data:formdata, contentType:false, processData:false}, function(data){
					if (data.status) {
						window.open(data.url, "_blank");
						window.location.reload();
					}else{
						Alerter.error('Erreur !', data.message);
					}
				}, 'json')
		})
		return false;
	});


})