import datetime
from django.shortcuts import render
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse, JsonResponse
from comptabilityApp.models import Mouvement, ReglementTricycle
from livraisonApp.models import LigneLivraison, Livraison, ModeLivraison, Tricycle
from productionApp.models import Brique, PerteBrique, Production
from commandeApp.models import GroupeCommande, Commande, LigneCommande, LigneConversion, ZoneLivraison, PrixZoneLivraison, Conversion
from clientApp.models import Client
from coreApp.models import Etat
from django.urls import reverse
from comptabilityApp.tools import mouvement_pour_sortie


def livraison(request):
    if request.method == "POST":
        datas = request.POST
        try :
            if "groupecommande_id" not in request.session:
                return JsonResponse({"status": False, "message": "Erreur lors de l'opération', veuillez recommencer !"})

            total = 0
            tableau = datas["listeproduits"].split(",")
            for item in tableau:
                if "=" in item:
                    id, livree, surplus, perte = item.split("=")
                    total += int(livree)
            if len(tableau) <= 0 :
                return JsonResponse({"status": False, "message": "Veuillez selectionner des produits et leur quantité pour faire la livraison !"})
            if total <= 0 :
                return JsonResponse({"status": False, "message": "Veuillez entrer des quantités valides pour la loivraison !"})
            
            
            groupe =  GroupeCommande.objects.get(pk = request.session["groupecommande_id"])
            test = True 
            for item in tableau:
                if "=" in item:
                    id, livree, surplus, perte = item.split("=")
                    brique = Brique.objects.get(pk = id)
                    stock = brique.stock(request.agence)
                    livree = int(livree)
                    if not ((0 < livree <= groupe.reste(brique)) and (livree <= stock >= (livree + int(surplus) + int(perte)))):
                        test = False
                        break
            
            if test :
                mode = ModeLivraison.objects.get(pk = datas["modelivraison"])
                if mode.etiquette != ModeLivraison.DEFAUT :
                    datas._mutable = True
                    datas["chauffeur"] = None
                    datas["vehicule"] = None

                livraison = Livraison.objects.create(
                    groupecommande = groupe,
                    agence = request.agence,
                    employe = request.user.employe,
                    lieu = datas["lieu"],
                    chauffeur_id = datas["chauffeur"],
                    vehicule_id = datas["vehicule"],
                    modelivraison = mode,
                    zone = ZoneLivraison.objects.get(pk = datas["zone"]),
                )

                if mode.etiquette == ModeLivraison.TRICYCLE :
                    tri = Tricycle.objects.create(
                        livraison = livraison,
                        fullname = datas["nom_tricycle"],
                        contact = datas["contact_tricycle"],
                        montant = datas["paye_tricycle"],
                        etat = Etat.objects.get(etiquette = Etat.EN_COURS)
                    )


                montant = 0
                for item in tableau:
                    if "=" in item:
                        id, livree, surplus, perte = item.split("=")
                        if int(livree) > 0 :
                            brique = Brique.objects.get(pk = id)
                            LigneLivraison.objects.create(
                                livraison = livraison,
                                brique = brique,
                                quantite = livree,
                                surplus = surplus,
                            );

                            if mode.etiquette != ModeLivraison.TRICYCLE :
                                paye = brique.cout("livraison", (livree+surplus), request.isferie)
                                if datas["chargement"] == "on":
                                    montant += paye / 2
                                if datas["dechargement"] == "on":
                                    montant += paye / 2
    
                            if int(perte) > 0 :
                                PerteBrique.objects.create(
                                    agence = request.agence,
                                    brique = brique,
                                    quantite = perte,
                                    comment = "Perte lors du chargement pour la livraison N°"+str(livraison.reference)
                                );

                if montant > 0:
                    production = Production.objects.get(date = datetime.datetime.now().date())
                    production.montant_livraison += montant
                    production.save();

                
                return JsonResponse({"status":True, "url":reverse("fiches:livraison", args=[livraison.id])})

            else:
                return JsonResponse({"status":False, "message":"Veuillez verifier la quantité de <b>"+brique.name+"</b> et/ou vous assurer qu'il y a suffisement de stock pour cette livraison !"})
        
        except Exception as e:
            print("----------------------------------------", e)
            return JsonResponse({"status":False, "message":"Une erreur s'est produite lors de l'operation, veuillez recommencer !"})






def retour_livraison(request):
    if request.method == "POST":
        datas = request.POST
        try :
            livraison = Livraison.objects.get(pk = datas["livraison"])
            tableau = datas["tableau"].split(",")

            if len(tableau) <= 0 :
                return JsonResponse({"status": False, "message": "Veuillez selectionner des produits et leur quantité pour faire la livraison !"})

            for item in tableau:
                if "=" in item:
                    id, perte = item.split("=")
                    perte = int(perte)
                    brique = Brique.objects.get(pk = id)
                    ligne = LigneLivraison.objects.get(livraison = livraison, brique = brique)
                    if not (ligne.quantite + ligne.surplus >= perte) :
                        return JsonResponse({"status": False, "message": "Veuillez à bien vérifier les quantités des différents produits livrés, certaines sont incorrectes (<b>"+brique.name+"</b>) !"})


            for item in tableau:
                if "=" in item:
                    id, perte = item.split("=")
                    perte = int(perte)
                    brique = Brique.objects.get(pk = id)
                    ligne = LigneLivraison.objects.get(livraison = livraison, brique = brique)
                    ligne.perte = perte
                    ligne.livree = ligne.quantite if ligne.surplus >= perte else ((ligne.quantite + ligne.surplus)-perte)
                    ligne.save()
                    ligne.reste = livraison.groupecommande.reste(brique)
                    ligne.save()
                    if (ligne.reste > 0 and livraison.groupecommande.etat.etiquette == Etat.TERMINE):
                        livraison.groupecommande.etat = Etat.objects.get(etiquette = Etat.EN_COURS)
                        livraison.groupecommande.save()

            livraison.comment = datas["comment"]
            livraison.nom_receptionniste = datas["nom_receptionniste"]
            livraison.contact_receptionniste = datas["contact_receptionniste"]
            livraison.datelivraison = datas["datelivraison"]
            livraison.etat = Etat.objects.get(etiquette = Etat.TERMINE)
            livraison.save()

            return JsonResponse({"status":True})

        except Exception as e:
            print("----------------------------------------", e)
            return JsonResponse({"status":False, "message":"Une erreur s'est produite lors de l'operation, veuillez recommencer !"})




def paye_tricycle(request):
    if request.method == "POST":
        datas = request.POST
        try :
            tricycle = Tricycle.objects.get(pk = datas["tricycle_id"])
            name = "Reglement de la paye du  tricycle "+ tricycle.fullname +" pour la livraison N°"+str(tricycle.livraison.reference)
            res = mouvement_pour_sortie(request, datas, name)
            if type(res) is Mouvement:
                ReglementTricycle.objects.create(
                    mouvement = res,
                    tricycle = tricycle
                )
                return JsonResponse({"status":True, "url":reverse("fiches:boncaisse", args=[res.id])})
            else:
                return JsonResponse(res)

        except Exception as e:
            print("Erreur valid tricycle", e)
            return JsonResponse({"status": False, "message":"Erreur lors de l'opération', veuillez recommencer !"})

