$(function(){

	$("#formAcompte").submit(function(event) {
		var url = "../ajax/crediter/";
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
		alerty.confirm("Voulez-vous vraiment regler toutes les dettes de ce client ? \n Le Recouvrement se fera via l'acompte de celui-ci. veuillez donc l'approvisionner. \n Le recouvrement se fera également dans la limite des fonds disponibles", {
			title: "Recouvrement de dettes",
			cancelLabel : "Non",
			okLabel : "OUI, valider",
		}, function(){
			var url = "../ajax/regler_toutes_dettes/";
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
		var url = "../ajax/rembourser/";
		alerty.confirm("Voulez-vous vraiment rembourser ce montant à ce client ?", {
			title: "rembourser l'acompte",
			cancelLabel : "Non",
			okLabel : "OUI, créditer",
		}, function(){
			alerty.prompt("Entrer votre mot de passe pour confirmer l'opération !", {
				title: 'Récupération du mot de passe !',
				inputType : "password",
				cancelLabel : "Annuler",
				okLabel : "Valider"
			}, function(password){
				var formdata = new FormData($("#formRembourser")[0]);
				formdata.append('password', password);
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
		})
		return false;
	});


})