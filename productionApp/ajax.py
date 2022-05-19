
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse, JsonResponse
import datetime
from coreApp.models import Etat
from productionApp.models import Production, Ressource
import traceback


def calcul_production(request):
    if request.method == "POST":
        ressources = Ressource.objects.filter(deleted = False, active = True)
        datas = request.POST
        tab = {}
        html = ""
        if request.societe.production_auto:
            productionday = Production.objects.get(date = datetime.datetime.now().date())
            for ligne in productionday.production_ligne.all():
                name = "prod-"+str(ligne.brique.id)
                if name in datas:
                    for ressource in ressources:
                        if str(ressource.id) in tab:
                            tab[str(ressource.id)] += ligne.brique.exigence(datas[name], ressource)
                        else:
                            tab[str(ressource.id)] = ligne.brique.exigence(datas[name], ressource)
            for ressource in ressources:
                context = {
                    "ressource": ressource,
                    "tab": tab
                }
                html += render_to_string("production/extra/auto_ressource.html", context, request)

        else:
            for ressource in ressources:
                name = "conso-"+str(ressource.id)
                tab[str(ressource.id)] = datas[name]

        request.session["tab"] = tab
        return HttpResponse(html)




def new_production(request):
    if request.method == "POST":
        datas = request.POST

        if "tab" not in request.session:
            return JsonResponse({"status": False, "message": "Une erreur s'est produite lors de l'opération, veuillez recommencer !"})
        
        tab = request.session["tab"]
        productionday = Production.objects.get(date = datetime.datetime.now().date())

        test = True;
        for ligne in productionday.production_ligneconsommation.all():
            if tab[str(ligne.ressource.id)] > (ligne.ressource.stock(request.agence) + ligne.quantite) :
                test = False
                break
            
        if not test:
            return JsonResponse({"status": False, "message": "Vous ne pouvez pas consommer plus de quantité de <b>"+ligne.ressource.name+"</b> que ce que vous n'en possédez !"})
            
        montant = 0
        for ligne in productionday.production_ligne.all():
            name = "prod-"+str(ligne.brique.id)
            ligne.quantite = int(datas[name] or 0)
            ligne.save()
            montant += ligne.brique.cout("production", int(datas[name]))

        for ligne in productionday.production_ligneconsommation.all():
            ligne.quantite = tab[str(ligne.ressource.id)]
            ligne.price = tab[str(ligne.ressource.id)] * ligne.ressource.cout(request.agence)
            ligne.save()

        productionday.comment = datas["comment"]
        productionday.montant_production = montant
        productionday.employe = request.user.employe
        productionday.etat = Etat.objects.get(etiquette = Etat.EN_COURS)
        productionday.save()

        return JsonResponse({"status":True})



def rangement(request):
    if request.method == "POST":
        datas = request.POST
        try:
            production = Production.objects.get(pk = datas["id"])
            test = True

            for ligne in production.production_ligne.all():
                name = "range-"+str(ligne.brique.id)
                if (ligne.quantite < int(datas[name])):
                    test = False
                    break

            if not test:
                return JsonResponse({"status": False, "message": "Vous ne pouvez pas rangé plus de quantité que ce que vous en avez produit !"})

            montant = 0
            for ligne in production.production_ligne.all():
                name = "range-"+str(ligne.brique.id)
                ligne.perte = ligne.quantite - int(datas[name])
                ligne.save()
                montant += ligne.brique.cout("rangement", int(datas[name]))

            production.montant_rangement = montant
            production.employe_rangement = request.user.employe
            production.date_rangement = datetime.datetime.now()
            production.etat = Etat.objects.get(etiquette = Etat.TERMINE)
            production.save()

            return JsonResponse({"status":True})

        except Exception as e:
            print("erreur :", e)
            return JsonResponse({"status": False, "message": "Une erreur s'est produite lors de l'opération, veuillez recommencer !"})