from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render
from commandeApp.models import Commande
from organisationApp.models import Employe
from django.http import  JsonResponse
from django.contrib.sessions.backends.db import SessionStore
from comptabilityApp.models import CategoryOperation, Operation, ReglementCommande, TypeMouvement, Mouvement, ModePayement, CompteClient
from comptabilityApp.tools import mouvement_pour_entree, mouvement_pour_sortie, mouvement_pour_sortie_client
from clientApp.models import Client
from authApp.tools import verify_password
# Create your views here.


def crediter(request):
    if request.method == "POST":
        datas = request.POST
        client = Client.objects.get(pk = request.session["client_id"])
        name = client.name +" a crédité son compte de "+datas["montant"]
        
        res = mouvement_pour_entree(request, datas, name)
        if type(res) is Mouvement:
            CompteClient.objects.create(
                    mouvement = res,
                    client = client
                )
        else:
            return JsonResponse(res)

    return JsonResponse({"status":True, "url" : "TODO" })




def rembourser(request):
    try:
        if request.method == "POST":
            datas = request.POST
            mode = ModePayement.objects.get(pk = datas["modepayement"])
            client = Client.objects.get(pk = request.session["client_id"])
            name = "remboursement du client "+client.name

            if not verify_password(request, datas["password"]):
                return JsonResponse({"status":False, "message" : "Le mot de passe est incorrect !" })

            res = mouvement_pour_sortie(request, datas, name)
            if type(res) is Mouvement:
                Operation.objects.create(
                    mouvement = res,
                    category = CategoryOperation.objects.get(etiquette = CategoryOperation.REFUND_CLIENT)
                )

                CompteClient.objects.create(
                    mouvement = res,
                    client = client,
                )
            else:
                return JsonResponse(res)

        return JsonResponse({"status":True, "url" : "TODO" })
    except Exception as e:
        print("-++++++++++++++++++++++++++++++", e)





def regler_toutes_dettes(request):
    try:
        if request.method == "POST":
            datas = {}
            client = Client.objects.get(pk = request.session["client_id"])
            mode = ModePayement.objects.get(etiquette = ModePayement.PRELEVEMENT)
            
            datas["password"] = request.POST["password"]
            datas["modepayement"] = mode.id
            datas["structure"] = ""
            datas["numero"] = ""

            if not verify_password(request, datas["password"]):
                return JsonResponse({"status":False, "message" : "Le mot de passe est incorrect !" })

            acompte = client.acompte_actuel()
            dette = client.dette_totale()
            while acompte > 0 and dette > 0 :
                for commande in Commande.objects.filter(groupecommande__client = client, deleted = False):
                    reste =  commande.reste_a_payer()
                    if reste > 0 and acompte > 0:
                        datas["montant"] = reste if acompte >= reste else acompte
                        name = "reglement de la commande N°"+commande.reference
                        res = mouvement_pour_sortie_client(request, datas, name)
                        if type(res) is Mouvement:
                            ReglementCommande.objects.create(
                                mouvement = res,
                                commande = commande
                            )
                            acompte = client.acompte_actuel()
                        else:
                            return JsonResponse(res)

                if acompte > 0:
                    dette = client.dette_totale()
                    datas["montant"] = dette if acompte >= dette else acompte
                    name = "reglement de la dette de "+client.name
                    res = mouvement_pour_sortie_client(request, datas, name)
                    if type(res) is Mouvement:
                        CompteClient.objects.create(
                            mouvement = res,
                            client = client,
                            is_dette = True
                        )
                    else:
                        return JsonResponse(res)

                acompte = client.acompte_actuel()
                print("-++++++++++++++++++++++++++++++", acompte)
                dette = client.dette_totale()

        return JsonResponse({"status":True})
        
    except Exception as e:
        print("-++++++++++++++++++++++++++++++", e)
        return JsonResponse({"status":False, "message":e})