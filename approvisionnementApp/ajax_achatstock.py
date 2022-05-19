
from django.urls.base import reverse
from approvisionnementApp.models import AchatStock, Approvisionnement, Fournisseur, LigneAchatStock, LigneApprovisionnement
from approvisionnementApp.views import achatstock
from comptabilityApp.models import CategoryOperation, CompteClient, CompteFournisseur, ModePayement, Mouvement, Operation, ReglementAchatStock, ReglementApprovisionnement
from comptabilityApp.tools import mouvement_pour_sortie, mouvement_pour_sortie_client, mouvement_pour_sortie_fournisseur
from coreApp.models import Etat
from productionApp.models import Brique
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.contrib.humanize.templatetags.humanize import intcomma
import datetime

def new_produit(request):
    if request.method == "POST":
        datas = request.POST
        try:
            brique = Brique.objects.get(pk = datas["id"])
            request.session[datas["id"]] = 1
            context = {
                "brique" : brique,
                "qte" : 1
            }
            html = render_to_string("appros/extra/ligne_achatstock.html", context, request)
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
        montant = 0
        for item in datas["tableau"].split(","):
            if "=" in item:
                id, qte, price = item.split("=")
                montant += int(price)

        avance = int(datas["avance"])
        mode = ModePayement.objects.get(pk = datas["modepayement"])
        if mode.etiquette == ModePayement.PRELEVEMENT:
            fournisseur = Fournisseur.objects.get(pk = datas["fournisseur"])
            acompte = fournisseur.acompte_actuel()
            avance =  montant if acompte >= montant else acompte

        total = montant - avance;

        request.session["montant"] = montant
        request.session["avance"] = avance
        request.session["total"] = total

        return HttpResponse("")




def total(request):
    if request.method == "POST":
        datas = {
            "montant":str(intcomma(request.session["montant"]))+" "+ request.societe.devise,
            "avance":str(intcomma(request.session["avance"]))+" "+ request.societe.devise,
            "total":str(intcomma(request.session["total"]))+" "+ request.societe.devise
        }
        return JsonResponse(datas)




def valider_achatstock(request):
    if request.method == "POST":
        datas = request.POST
        datas._mutable = True
        try:
            if datas["transport"] == "" : datas["transport"] = 0
            mode = ModePayement.objects.get(pk = datas["modepayement"])
            fournisseur = Fournisseur.objects.get(pk = datas["fournisseur"])

            tableau = datas["tableau"].split(",")
            montant = request.session["montant"]
            avance = int(datas["avance"])
            if mode.etiquette == ModePayement.PRELEVEMENT:
                avance = 0

            if len(tableau) <= 0 :
                return JsonResponse({"status": False, "message": "Veuillez selectionner des briques et leur quantité pour passer la commande !"})

            total = 0
            for item in tableau:
                if "=" in item:
                    id, qte, price = item.split("=")
                    brique = Brique.objects.get(pk = id)
                    total += int(qte)

            if total <= 0 :
                return JsonResponse({"status": False, "message": "Veuillez selectionner des briques et leur quantité pour passer la commande ! "})

            if not (0 <= montant >= avance) :
                return JsonResponse({"status": False, "message": "Veuillez verifier le montant et l'avance por cet achat de stock ! "})

            if not ((mode.etiquette == ModePayement.PRELEVEMENT) or (mode.etiquette != ModePayement.PRELEVEMENT and 0 < avance <= montant)):
                return JsonResponse({"status": False, "message": "L'avance de la commande est incorrect, verifiez-le!"})


            if mode.etiquette == ModePayement.PRELEVEMENT:
                if not (request.agence_compte.solde_actuel() >= (avance + int(datas["transport"]))):
                    return JsonResponse({"status": False, "message": "Le solde du compte est insuffisant pour regler l'avance et les frais de transport de l'achat de stock !"})
            else:
                if not (request.agence_compte.solde_actuel() >=  int(datas["transport"])):
                    return JsonResponse({"status": False, "message": "Le solde du compte est insuffisant pour regler les frais de transport de l'achat de stock !"})

            if int(datas["transport"]) > 0:
                title = "Frais de transport"
                comment = "Frais de transport pour l'achat de stock"
                datas["montant"] = int(datas["transport"])
                datas["modepayement"] = ModePayement.objects.get(etiquette = ModePayement.ESPECES).id
                res = mouvement_pour_sortie(request, datas, title, comment)
                if type(res) is Mouvement:
                    Operation.objects.create(
                        mouvement = res,
                        category = CategoryOperation.objects.get(etiquette = CategoryOperation.TRANSPORT)
                    )
                else:
                    return JsonResponse(res)

            res = None
            if mode.etiquette == ModePayement.PRELEVEMENT :
                acompte = fournisseur.acompte_actuel()
                lavance = montant if acompte >= montant else acompte
                if lavance > 0 :
                    title = "Avance sur achat de stock"
                    comment = "Avance sur réglement de la facture pour l'achat de stock"
                    datas["montant"] = lavance
                    res = mouvement_pour_sortie_fournisseur(request, datas, title, comment)
                    if type(res) is not Mouvement:
                        return JsonResponse(res)

            else:
                title= "Avance sur achat de stock"
                comment = "Avance sur réglement de la facture pour l'achat de stock"
                datas["montant"] = avance
                res = mouvement_pour_sortie(request, datas, title, comment)
                if type(res) is not Mouvement:
                    return JsonResponse(res)


            etat = Etat.objects.get(etiquette = datas["etat"]) 
            achat = AchatStock.objects.create(
                fournisseur = fournisseur,
                agence = request.agence,
                employe = request.user.employe,
                montant = montant,
                transport = datas["transport"],
                etat = etat,
                datelivraison = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if etat.etiquette == Etat.TERMINE else None,
            )


            for item in tableau:
                if "=" in item:
                    id, qte, price = item.split("=")
                    brique = Brique.objects.get(pk = id)
                    LigneAchatStock.objects.create(
                        brique = brique,
                        quantite = qte,
                        price = price,
                        achatstock = achat
                    );

            

            if type(res) is Mouvement:
                ReglementAchatStock.objects.create(
                    mouvement = res,
                    achatstock = achat
                )



            achat.acompte_fournisseur = fournisseur.acompte_actuel();
            achat.dette_fournisseur = fournisseur.dette_totale();
            achat.save();

            return JsonResponse({"status": True, "url1":reverse("fiches:achatstock", args=[achat.id])})

        except Exception as e:
            print("Erreur valid commande", e)
            return JsonResponse({"status": False, "message":str(e)})





def terminer_achat(request):
    if request.method == "POST":
        try:
            datas = request.POST

            tableau = datas["tableau"].split(",")
            total = 0
            for item in tableau:
                if "=" in item:
                    id, qte = item.split("=")
                    ligne = LigneAchatStock.objects.get(pk = id)
                    total += int(qte)
                    if not (ligne.quantite >= int(qte)):
                        return JsonResponse({"status": False, "message": "La quantité pour "+ligne.brique.name+" est incorrecte ! "})

            if total <= 0 :
                return JsonResponse({"status": False, "message": "Veuillez renseigner les quantités des briques qui ont été livrées! "})


            for item in tableau:
                if "=" in item:
                    id, qte = item.split("=")
                    ligne = LigneAchatStock.objects.get(pk = id)
                    ligne.quantite_recu = int(qte)
                    ligne.save()

            ligne.achatstock.etat =  Etat.objects.get(etiquette = Etat.TERMINE)
            ligne.achatstock.save()



            return JsonResponse({"status": True})

        except Exception as e:
            print("Erreur valid achat", e)
            #return JsonResponse({"status": False, "message":"Erreur lors de la validation de la commande, veuillez recommencer !"})
            return JsonResponse({"status": False, "message":str(e)})




def regler_achat(request):
    if request.method == "POST":
        datas = request.POST
        try :
            achat = AchatStock.objects.get(pk = datas["achat_id"])
            title = "Reglement Achat de brique"
            comment = "Reglement de l'achat de stock N°"+str(achat.id)
            res = mouvement_pour_sortie_fournisseur(request, datas, title, comment)
            if type(res) is Mouvement:
                ReglementAchatStock.objects.create(
                    mouvement = res,
                    achatstock = achat
                )
                return JsonResponse({"status":True, "url":reverse("fiches:boncaisse", args=[res.id])})
            else:
                return JsonResponse(res)

        except Exception as e:
            print("Erreur valid achat", e)
            return JsonResponse({"status": False, "message":"Erreur lors de l'opération', veuillez recommencer !"})
