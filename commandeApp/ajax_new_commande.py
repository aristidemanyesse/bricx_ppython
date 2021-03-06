from django.shortcuts import render
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse, JsonResponse
from comptabilityApp.tools import mouvement_pour_entree, mouvement_pour_entree, mouvement_pour_sortie_client
from productionApp.models import Brique
from commandeApp.models import GroupeCommande, Commande, LigneCommande, LigneConversion, ZoneLivraison, PrixZoneLivraison, Conversion
from comptabilityApp.models import CompteClient, ModePayement, Mouvement, ReglementCommande
from clientApp.models import Client
from coreApp.models import Etat
from django.urls import reverse
from django.utils.translation import gettext as _

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

        avance = int(datas["avance"] if datas["avance"] != "" else 0)

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
            total = request.session["montant"] + request.session["tva"]
            avance = int(datas["avance"] if datas["avance"] != "" else 0)
            
            if len(tableau) <= 0 :
                return JsonResponse({"status": False, "message": _("Veuillez selectionner des produits et leur quantit?? pour passer la commande !")})

            if total <= 0 :
                return JsonResponse({"status": False, "message": _("Veuillez verifier le montant de la commande ! ")})

            if not ((mode.etiquette == ModePayement.PRELEVEMENT) or (mode.etiquette != ModePayement.PRELEVEMENT and 0 < avance <= total)):
                return JsonResponse({"status": False, "message": _("L'avance de la commande est incorrect, verifiez-le!")})

            if mode.etiquette == ModePayement.PRELEVEMENT :
                avance = client.acompte_actuel()

            seuil = (client.seuil_credit or 0) if (client.seuil_credit or 0) > 0 else request.societe.seuil_credit
            if not (seuil == 0 or avance == total or ((total - avance + client.dette_totale()) <= seuil)):
                return JsonResponse({"status": False, "message": _("Le cr??dit restant pour la commande ne doit pas exc??der ")+intcomma(seuil)+" "+request.societe.devise+_(" pour ce client ")})

            if "groupecommande_id" in request.session:
                groupe = GroupeCommande.objects.get(pk = request.session["groupecommande_id"])
            else:
                groupe = GroupeCommande.objects.create(
                    client = client,
                    agence = request.agence
                )

            if mode.etiquette == ModePayement.PRELEVEMENT :
                avance = total if avance >= total else avance
                print("--------------------------", avance)
                if avance > 0 :
                    title = _("Avance sur commande")
                    comment = _("Avance sur r??glement de la facture pour la commande ")
                    datas["montant"] = avance
                    res = mouvement_pour_sortie_client(request, datas, title, comment)
                    if type(res) is not Mouvement:
                        return JsonResponse(res)
                    

            else:
                title = _("Avance sur commande")
                comment = _("Avance sur r??glement de la facture pour la commande ")
                datas["montant"] = avance
                res = mouvement_pour_entree(request, datas, title, comment)
                if type(res) is not Mouvement:
                    return JsonResponse(res)
                
            
            commande = Commande.objects.create(
                groupecommande = groupe,
                agence = request.agence,
                employe = request.user.employe,
                montant = total,
                avance = avance,
                taux_tva = request.societe.tva,
                tva = request.session["tva"],
                datelivraison = datas["datelivraison"],
                comment = datas["comment"],
                lieu = datas["lieu"],
                zone = ZoneLivraison.objects.get(pk = datas["zone"]),
                acompte_client = client.acompte_actuel(),
                dette_client = client.dette_totale()
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
                    
            if avance > 0:
                # if mode.etiquette == ModePayement.PRELEVEMENT :           
                #     CompteClient.objects.create(
                #         client = groupe.client,
                #         mouvement = res
                #     )
                # else:
                ReglementCommande.objects.create(
                    mouvement = res,
                    commande = commande
                )
            
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
            title = "Reglement de facture commande"
            comment = "Reglement de la commande N??"+str(commande.id)
            res = mouvement_pour_sortie_client(request, datas, title, comment)
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
            return JsonResponse({"status": False, "message": _("Erreur lors de l'op??ration', veuillez recommencer !")})





def changer_produit(request):
    if request.method == "POST":
        datas = request.POST
        try :
            if "groupecommande_id" not in request.session:
                return JsonResponse({"status": False, "message": _("Erreur lors de l'op??ration', veuillez recommencer !")})

            total = 0
            tableau = datas["tableau"].split(",")
            for item in tableau:
                if "=" in item:
                    id, qte = item.split("=")
                    total += int(qte) if qte != "" else 0
            if len(tableau) <= 0 :
                return JsonResponse({"status": False, "message": _("Veuillez selectionner des produits et leur quantit?? pour passer la commande !")})
            if total <= 0 :
                return JsonResponse({"status": False, "message": _("Veuillez entrer des quantit??s valides pour la conversion !")})
            
            GroupeCommande.objects.filter(pk = request.session["groupecommande_id"]).update(etat = Etat.objects.get(etiquette = Etat.TERMINE))
            old = GroupeCommande.objects.get(pk = request.session["groupecommande_id"])
            comm = old.commande_groupecommande.filter(deleted = False).first()
            new = GroupeCommande.objects.create(
                    client = old.client,
                    agence = request.agence,
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
                is_conversion = True
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
                    qte = qte if qte != "" else 0
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
            return JsonResponse({"status": False, "message": _("Erreur lors de l'op??ration', veuillez recommencer :")+ str(e)})
