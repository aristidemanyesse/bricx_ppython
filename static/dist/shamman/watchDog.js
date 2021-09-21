
$(function(){
	$(document).idleTimer(13 * 60 * 1000);
	$(document).on("idle.idleTimer", function(event, elem, obj){
		window.location.href = "../../main/access/locked";
	});

	$("a#btn-deconnexion").click(function(event) {
		alerty.confirm("Voulez-vous vraiment vous deconnecter ???", {
			title: "Deconnexion",
			cancelLabel : "Non",
			okLabel : "OUI, me deconnecter",
		}, function(){
			window.location.href = "../../main/access/logout";
		})
	});



	horloge = function(){
		tabMois = ["Janvier", "Février", "Mars","Avril","Mai","Juin", "Juillet", "Août","Septembre","Octobre","Novembre", "Décembre"];
		tabSemaine = ["Dimanche", "Lundi", "Mardi", "Mercredi","jeudi","Vendredi","Samedi"];

		ladate = new Date();
		j = ladate.getDay();
		jj = concate0(ladate.getDate());
		MM = concate0(ladate.getMonth());
		yy = ladate.getFullYear();
		hh = concate0(ladate.getHours());
		mm = concate0(ladate.getMinutes());
		ss = concate0(ladate.getSeconds());

		jour = tabSemaine[parseInt(j)];
		MM = tabMois[parseInt(MM)];

		$("#heure_actu").html(hh+':'+mm+':'+ss)
		$("#date_actu").html(jour+' '+jj+' '+MM+' '+yy)
	}

	setInterval(function(){
		horloge();
	}, 1000);


})