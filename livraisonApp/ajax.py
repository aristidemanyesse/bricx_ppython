from django.shortcuts import render
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse, JsonResponse
from livraisonApp.models import LigneLivraison, ModeLivraison
from productionApp.models import Brique
from commandeApp.models import GroupeCommande, Commande, LigneCommande, LigneConversion, ZoneLivraison, PrixZoneLivraison, Conversion
from clientApp.models import Client
from coreApp.models import Etat
from django.urls import reverse



def livraison(request):
    pass
#     if request.method == "POST":
#         datas = request.POST
#         try :
#             if "groupecommande_id" not in request.session:
#                 return JsonResponse({"status": False, "message": "Erreur lors de l'opération', veuillez recommencer !"})

#             total = 0
#             tableau = datas["tableau"].split(",")
#             for item in tableau:
#                 if "=" in item:
#                     id, livree, surplus, perte = item.split("=")
#                     total += int(livree)
#             if len(tableau) <= 0 :
#                 return JsonResponse({"status": False, "message": "Veuillez selectionner des produits et leur quantité pour faire la livraison !"})
#             if total <= 0 :
#                 return JsonResponse({"status": False, "message": "Veuillez entrer des quantités valides pour la loivraison !"})
            
#             groupe = GroupeCommande.objects.get(pk = request.session["groupecommande_id"])

#             livraison = Livraison.objects.create(
#                 groupecommande = groupe,
#                 agence = request.agence,
#                 employe = request.user.employe,
#                 lieu = datas["lieu"],
#                 comment = datas["comment"],
#                 mode = ModeLivraison.objects.get(pk = datas["zone"]),
#                 zone = ZoneLivraison.objects.get(pk = datas["zone"]),
#             )

#             for item in tableau:
#                 if "=" in item:
#                     id, livree, surplus, perte = item.split("=")
#                     if int(livree) > 0 :
#                         brique = Brique.objects.get(pk = id)
#                         LigneLivraison.objects.create(
#                             livraison = livraison,
#                             brique = brique,
#                             quantite = livree,
#                             surplus = surplus,
#                         );

#                         PerteBrique.objects.create(
#                             agence = request.agence,
#                             brique = brique,
#                             quantite = perte,
#                         );

#     $params = PARAMS::findLastId();
# 	if (getSession("commande-encours") != null) {
# 		$datas = GROUPECOMMANDE::findBy(["id ="=>getSession("commande-encours")]);
# 		if (count($datas) > 0) {
# 			$groupecommande = $datas[0];
# 			$groupecommande->actualise();


# 			$listeproduits = explode(",", $listeproduits);
# 			if (count($listeproduits) > 0) {
# 				$tests = $listeproduits;
# 				foreach ($tests as $key => $value) {
# 					$lot = explode("-", $value);
# 					$id = $lot[0];
# 					$qte = $lot[1];
# 					$surplus = $lot[2];
# 					$perte = end($lot);
# 					$produit = PRODUIT::findBy(["id ="=>$id])[0];
# 					$stock = $produit->stock(PARAMS::DATE_DEFAULT, dateAjoute(1), getSession("agence_connecte_id"));
# 					if ($qte >= 0 && $groupecommande->reste($produit->id) >= $qte && $qte <= $stock && (($qte + $surplus + $perte) <= $stock)) {
# 						unset($tests[$key]);
# 					}
# 				}
# 				if (count($tests) == 0) {
# 					$livraison = new LIVRAISON();
# 					if ($vehicule_id <= VEHICULE::TRICYCLE) {
# 						$_POST["chauffeur_id"] = 0;
# 					}
# 					$livraison->hydrater($_POST);
# 					$livraison->groupecommande_id = $groupecommande->id;
# 					$data = $livraison->enregistre();
# 					if ($data->status) {
# 						$montant = 0;

# 						foreach ($listeproduits as $key => $value) {
# 							$lot = explode("-", $value);
# 							$id = $lot[0];
# 							$qte = $lot[1];
# 							$surplus = $lot[2];
# 							$perte = end($lot);

# 							if ($vehicule_id > VEHICULE::TRICYCLE) {
# 								$paye = $produit->coutProduction("livraison", $qte);
# 								if (isset($chargement) && $chargement == "on") {
# 									$montant += $paye / 2;
# 								}

# 								if (isset($dechargement) && $dechargement == "on") {
# 									$montant += $paye / 2;
# 								}
# 							}
							
# 							$lignelivraison = new LIGNELIVRAISON;
# 							$lignelivraison->livraison_id = $livraison->id;
# 							$lignelivraison->produit_id = $id;
# 							$lignelivraison->quantite = $qte;
# 							$lignelivraison->surplus = $surplus;
# 							$lignelivraison->enregistre();

# 							$laperte = new PERTEPRODUIT;
# 							$laperte->typeperte_id = TYPEPERTE::CHARGEMENT;
# 							$laperte->produit_id = $id;
# 							$laperte->quantite = $perte;
# 							$laperte->comment = "Perte lors du chargement pour la livraison N°$livraison->reference";
# 							$laperte->enregistre();
# 						}

# 						$production = PRODUCTION::today();
# 						$production->montant_livraison += $montant;
# 						$production->save();

# //////////////////////////////////////////

# 						$data = $livraison->save();
# 						$data->setUrl("fiches", "master", "bonlivraison", $data->lastid);				
# 					}	
# 				}else{
# 					$data->status = false;
# 					$data->message = "Veuillez à bien vérifier les quantités des différents produits à livrer, certaines sont incorrectes !";
# 				}
# 			}else{
# 				$data->status = false;
# 				$data->message = "Veuillez selectionner des produits et leur quantité pour passer la commande !";
# 			}
# 		}else{
# 			$data->status = false;
# 			$data->message = "Une erreur s'est produite lors de l'operation, veuillez recommencer !";
# 		}
# 	}else{
# 		$data->status = false;
# 		$data->message = "Une erreur s'est produite lors de l'operation, veuillez recommencer !";
# 	}
# 	echo json_encode($data);