import datetime
from django.http import JsonResponse
from comptabilityApp.models import CategoryOperation, Compte, ModePayement, Mouvement, Operation, ReglementCommande, TypeOperationCaisse
from comptabilityApp.tools import mouvement_pour_entree, mouvement_pour_sortie, mouvement_pour_sortie_client
from django.urls import reverse
from authApp.tools import verify_password
from coreApp.models import Etat


def operation(request):
    if request.method == "POST":
        datas = request.POST
        try :
            cat = CategoryOperation.objects.get(pk = datas["category"])
            title = cat.name
            if cat.type.etiquette == TypeOperationCaisse.DEPOT:
                res = mouvement_pour_entree(request, datas, title, datas["comment"])
            else:
                res = mouvement_pour_sortie(request, datas, title, datas["comment"])
                
            if type(res) is Mouvement:
                Operation.objects.create(
                    mouvement = res,
                    category = cat
                )
                return JsonResponse({"status":True, "url":reverse("fiches:boncaisse", args=[res.id])})
            else:
                return JsonResponse(res)

        except Exception as e:
            print("Erreur valid commande", e)
            return JsonResponse({"status": False, "message":"Erreur lors de l'opération', veuillez recommencer !"})




def transfert(request):
    if request.method == "POST":
        datas = request.POST
        try :

            if not verify_password(request, datas["password"]):
                return JsonResponse({"status":False, "message" : "Le mot de passe est incorrect !" })

            datas._mutable = True
            datas["modepayement"] = ModePayement.objects.get(etiquette = ModePayement.ESPECES).id
            datas["structure"] = ""
            datas["numero"] = ""

            cat = CategoryOperation.objects.get(etiquette = CategoryOperation.TRANSFERT_RETRAIT)
            title = cat.name
            res = mouvement_pour_sortie(request, datas, title, datas["comment"])
            if type(res) is Mouvement:
                Operation.objects.create(
                    mouvement = res,
                    category = cat
                )

                cat = CategoryOperation.objects.get(etiquette = CategoryOperation.TRANSFERT_DEPOT)
                title = cat.name
                request.agence_compte = Compte.objects.get(pk = datas["compte"])
                res = mouvement_pour_entree(request, datas, title, datas["comment"])
                request.agence_compte =  request.agence.agence_compte.all().first()
                if type(res) is Mouvement:
                    Operation.objects.create(
                        mouvement = res,
                        category = cat
                    )
                    return JsonResponse({"status":True})

                else:
                    return JsonResponse(res)

            else:
                return JsonResponse(res)
                

        except Exception as e:
            print("Erreur valid commande", e)
            return JsonResponse({"status": False, "message":"Erreur lors de l'opération', veuillez recommencer !"})





def valider_mouvement(request):
    if request.method == "POST":
        datas = request.POST
        try :

            if not verify_password(request, datas["password"]):
                return JsonResponse({"status":False, "message" : "Le mot de passe est incorrect !" })

            mouvement = Mouvement.objects.get(pk = datas["id"])
            mouvement.etat = Etat.objects.get(etiquette = Etat.TERMINE)
            mouvement.date_approbation = datetime.datetime.now()
            mouvement.save()

            return JsonResponse({"status":True})

        except Exception as e:
            print("Erreur valid commande", e)
            return JsonResponse({"status": False, "message":"Erreur lors de l'opération', veuillez recommencer !"})