from django.shortcuts import render
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse, JsonResponse
from comptabilityApp.tools import mouvement_pour_entree, mouvement_pour_sortie, mouvement_pour_sortie_client
from productionApp.models import Brique
from commandeApp.models import GroupeCommande, Commande, LigneCommande, LigneConversion, ZoneLivraison, PrixZoneLivraison, Conversion
from comptabilityApp.models import CompteClient, ModePayement, Mouvement, ReglementCommande
from clientApp.models import Client
from coreApp.models import Etat
from django.urls import reverse

from django.contrib.humanize.templatetags.humanize import intcomma
# Create your views here.


def new_produit(request):
    if request.method == "POST":
        datas = request.POST
        try:
            brique = Brique.objects.get(pk = datas["id"])
            pz = PrixZoneLivraison.objects.get(brique = brique, zone_id = datas["zone"])
            request.session[datas["id"]] = 1
            request.session["zone"] = datas["zone"]
            context = {
                "brique" : brique,
                "pz" : pz,
                "price" : pz.price,
                "qte" : 1
            }
            html = render_to_string("commande/extra/ligne_commande.html", context, request)
            return HttpResponse(html)

        except Exception as e:
            return JsonResponse({"status":False, "message":e})



def delete_ligne(request):
    if request.method == "POST":
        id = request.POST["id"]
        if id in request.session:
            del request.session[id]
        return HttpResponse("")



def actualise(request):
    if request.method == "POST":
        datas = request.POST
        html = ""
        montant = 0
        for item in datas["tableau"].split(","):
            if "=" in item:
                id, qte = item.split("=")
                brique = Brique.objects.get(pk = id)
                pz = PrixZoneLivraison.objects.get(brique = brique, zone_id = datas["zone"])
                price = int(pz.price) * int(qte)
                montant += price
                context = {
                    "brique" : brique,
                    "pz" : pz,
                    "price" : price,
                    "qte" : qte
                }
                html += render_to_string("commande/extra/ligne_commande.html", context, request)

        avance = int(datas["avance"])

        tva = (montant * request.societe.tva) / 100
        total = montant + tva;
        total -= avance


        request.session["tva"] = tva
        request.session["montant"] = montant
        request.session["avance"] = avance
        request.session["total"] = total

        return HttpResponse(html)




def total(request):
    if request.method == "POST":
        datas = {
            "tva":str(intcomma(request.session["tva"])) +" "+ request.societe.devise,
            "montant":str(intcomma(request.session["montant"]))+" "+ request.societe.devise,
            "avance":str(intcomma(request.session["avance"]))+" "+ request.societe.devise,
            "total":str(intcomma(request.session["total"]))+" "+ request.societe.devise
        }
        return JsonResponse(datas)





def valider_commande(request):
    if request.method == "POST":
        datas = request.POST
        datas._mutable = True
        try:
            client = Client.objects.get(pk = request.session["client_id"])
            mode = ModePayement.objects.get(pk = datas["modepayement"])

            tableau = datas["listeproduits"].split(",")
            total = request.session["montant"]
            avance = int(datas["avance"])
            
            if len(tableau) <= 0 :
                return JsonResponse({"status": False, "message": "Veuillez selectionner des produits et leur quantité pour passer la commande !"})

            if total <= 0 :
                return JsonResponse({"status": False, "message": "Veuillez verifier le montant de la commande ! "})

            if not ((mode.etiquette == ModePayement.PRELEVEMENT) or (mode.etiquette != ModePayement.PRELEVEMENT and 0 < avance <= total)):
                return JsonResponse({"status": False, "message": "L'avance de la commande est incorrect, verifiez-le!"})

            if mode.etiquette == ModePayement.PRELEVEMENT :
                avance = client.acompte_actuel()

            seuil = client.seuil_credit if client.seuil_credit > 0 else request.societe.seuil_credit
            if not (avance == total or ((total - avance + client.dette_totale()) <= seuil)):
                return JsonResponse({"status": False, "message": "Le crédit restant pour la commande ne doit pas excéder "+intcomma(seuil)+" "+request.societe.devise+" pour ce client "})

            if "groupecommande_id" in request.session:
                groupe = GroupeCommande.objects.get(pk = request.session["groupecommande_id"])
            else:
                groupe = GroupeCommande.objects.create(
                    client = client,
                    agence = request.agence
                )


            commande = Commande.objects.create(
                groupecommande = groupe,
                agence = request.agence,
                employe = request.user.employe,
                montant = total,
                tva = request.session["tva"],
                datelivraison = datas["datelivraison"],
                comment = datas["comment"],
                lieu = datas["lieu"],
                zone = ZoneLivraison.objects.get(pk = datas["zone"])
            )

            for item in tableau:
                if "=" in item:
                    id, qte = item.split("=")
                    brique = Brique.objects.get(pk = id)
                    pz = PrixZoneLivraison.objects.get(brique = brique, zone_id = datas["zone"])
                    price = int(pz.price) * int(qte)
                    LigneCommande.objects.create(
                        brique = brique,
                        quantite = qte,
                        price = price,
                        commande = commande
                    );


            if mode.etiquette == ModePayement.PRELEVEMENT :
                commande.avance = total if avance >= total else avance
                if commande.avance > 0 :
                    name = "Avance sur réglement de la facture pour la commande N°"+str(commande.reference);
                    datas["montant"] = commande.avance
                    res = mouvement_pour_sortie_client(request, datas, name)
                    if type(res) is Mouvement:
                        CompteClient.objects.create(
                            mouvement = res,
                            client = client
                        )
                    else:
                        return JsonResponse(res)

            else:
                name = "Avance sur réglement de la facture pour la commande N°"+str(commande.reference);
                datas["montant"] = avance
                res = mouvement_pour_sortie(request, datas, name)
                if type(res) is Mouvement:
                    ReglementCommande.objects.create(
                        mouvement = res,
                        commande = commande
                    )
                else:
                    return JsonResponse(res)


            commande.acompte_client = client.acompte_actuel();
            commande.dette_client = client.dette_totale();
            commande.save();

            return JsonResponse({"status": True, "url1":reverse("fiches:commande", args=[commande.id])})

        except Exception as e:
            print("Erreur valid commande", e)
            #return JsonResponse({"status": False, "message":"Erreur lors de la validation de la commande, veuillez recommencer !"})
            return JsonResponse({"status": False, "message":str(e)})




def regler_commande(request):
    if request.method == "POST":
        datas = request.POST
        try :
            commande = Commande.objects.get(pk = datas["commande_id"])
            name = "Reglement de la commande N°"+str(commande.reference)
            res = mouvement_pour_sortie_client(request, datas, name)
            if type(res) is Mouvement:
                ReglementCommande.objects.create(
                    mouvement = res,
                    commande = commande
                )
                return JsonResponse({"status":True, "url":reverse("fiches:boncaisse", args=[res.id])})
            else:
                return JsonResponse(res)

        except Exception as e:
            print("Erreur valid commande", e)
            return JsonResponse({"status": False, "message":"Erreur lors de l'opération', veuillez recommencer !"})





def changer_produit(request):
    if request.method == "POST":
        datas = request.POST
        try :
            if "groupecommande_id" not in request.session:
                return JsonResponse({"status": False, "message": "Erreur lors de l'opération', veuillez recommencer !"})

            total = 0
            tableau = datas["tableau"].split(",")
            for item in tableau:
                if "=" in item:
                    id, qte = item.split("=")
                    total += int(qte)
            if len(tableau) <= 0 :
                return JsonResponse({"status": False, "message": "Veuillez selectionner des produits et leur quantité pour passer la commande !"})
            if total <= 0 :
                return JsonResponse({"status": False, "message": "Veuillez entrer des quantités valides pour la conversion !"})
            
            GroupeCommande.objects.filter(pk = request.session["groupecommande_id"]).update(etat = Etat.objects.get(etiquette = Etat.TERMINE))
            old = GroupeCommande.objects.get(pk = request.session["groupecommande_id"])
            comm = old.commande_groupecommande.filter(deleted = False).first()
            new = GroupeCommande.objects.create(
                    client = old.client,
                    agence = request.agence
                )

            commande = Commande.objects.create(
                groupecommande = new,
                agence = request.agence,
                employe = request.user.employe,
                montant = 0,
                tva = comm.tva,
                datelivraison = old.datelivraison,
                lieu = comm.lieu,
                zone = comm.zone,
            )

            conversion = Conversion.objects.create(
                groupecommande_old = old,
                groupecommande_new = new,
                agence = request.agence,
                employe = request.user.employe,
            )

            for item in tableau:
                if "=" in item:
                    id, qte = item.split("=")
                    if int(qte) > 0 :
                        brique = Brique.objects.get(pk = id)
                        pz = PrixZoneLivraison.objects.get(brique = brique, zone = commande.zone)
                        price = int(pz.price) * int(qte)
                        LigneCommande.objects.create(
                            brique = brique,
                            quantite = qte,
                            price = price,
                            commande = commande
                        );

                    LigneConversion.objects.create(
                        brique = brique,
                        quantite_avant = old.reste(brique),
                        quantite_apres = qte,
                        conversion = conversion
                    );

            return JsonResponse({"status":True})

        except Exception as e:
            print("Erreur valid conversion", e)
            return JsonResponse({"status": False, "message":"Erreur lors de l'opération', veuillez recommencer !"})
