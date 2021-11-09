from django.db.models.aggregates import Sum
from django.shortcuts import render

from livraisonApp.models import Tricycle
from .models import Brique, PerteBrique, PerteRessource, Production, Ressource, LigneProduction, LigneConsommation, TypePerte
import datetime
# Create your views here.


def productions(request):
    if request.method == "GET":
        if 'tab' in request.session:
            del request.session['tab']
            
        briques = Brique.objects.filter(deleted = False)
        ressources = Ressource.objects.filter(deleted = False)
        try:
            productionday = Production.objects.get(date = datetime.datetime.now().date())
        except Exception as e:
            productionday = Production.objects.create(
                agence = request.agence,
                employe = request.user.employe,
                date = datetime.datetime.now().date()
            )

        debut = datetime.date.fromisoformat(request.session["date1"])
        fin = datetime.date.fromisoformat(request.session["date2"]) + datetime.timedelta(days= 1)

        context = {
            "productions" : Production.objects.filter(deleted = False, date__range = (debut, fin)),
            "productionday" : productionday,
            "briques" : briques,
            "ressources" : ressources
        }
        return render(request, "production/pages/productions.html", context)




def stock_brique(request):
    if request.method == "GET":
        dates = {}

        date = datetime.date.fromisoformat(request.session["date1"])
        debut = date
        fin = datetime.date.fromisoformat(request.session["date2"])
    
        while date <= fin:
            date_ = date + datetime.timedelta(days = 1)
            datas = {}
            for brique in Brique.objects.filter(deleted = False, active=True):
                datas[brique] = {
                    "stock"     : brique.stock(request.agence, date_), 
                    "production": brique.production(request.agence, date, date_), 
                    "achat"     : brique.achat(request.agence, date, date_), 
                    "livree"    : brique.livraison(request.agence, date, date_), 
                    "perteR"    : brique.perte_rangement(request.agence, date, date_), 
                    "perteL"    : brique.perte_livraison(request.agence, date, date_), 
                    "perteA"     : brique.perte_autre(request.agence, date, date_), 
                }
            dates[date] = datas
            date += datetime.timedelta(days=1)

        datas = {}
        for brique in Brique.objects.filter(deleted = False, active=True):
            datas[brique] = brique.stock(request.agence)

        context = {
            "dates" : dates,
            "debut" : debut,
            "fin" : fin,
            "briques" : datas,
            "types" : TypePerte.objects.filter(deleted = False)
        }
        return render(request, "production/pages/stock_brique.html", context)



def stock_ressource(request):
    if request.method == "GET":
        dates = {}

        date = datetime.date.fromisoformat(request.session["date1"])
        debut = date
        fin = datetime.date.fromisoformat(request.session["date2"])
    
        while date <= fin:
            date_ = date + datetime.timedelta(days = 1)
            datas = {}
            for ressource in Ressource.objects.filter(deleted = False, active=True):
                datas[ressource] = {
                    "stock"    : ressource.stock(request.agence, date_), 
                    "achat"    : ressource.achat(request.agence, date, date_), 
                    "consommee": ressource.consommation(request.agence, date, date_), 
                    "perte"    : ressource.perte(request.agence, date, date_), 
                }
            dates[date] = datas
            date += datetime.timedelta(days=1)

        datas = {}
        for ressource in Ressource.objects.filter(deleted = False, active=True):
            data = {}
            data["stock"] = ressource.stock(request.agence)
            data["estimation"] = ressource.estimation(request.agence)
            datas[ressource] = data


        context = {
            "dates" : dates,
            "debut" : debut,
            "fin" : fin,
            "ressources" : datas,
            "types" : TypePerte.objects.filter(deleted = False)
        }
        return render(request, "production/pages/stock_ressource.html", context)




def perte_brique(request):
    if request.method == "GET":
        debut = datetime.date.fromisoformat(request.session["date1"])
        fin = datetime.date.fromisoformat(request.session["date2"]) + datetime.timedelta(days= 1)

        pertes = PerteBrique.objects.filter(deleted = False, agence = request.agence, created_at__range = (debut, fin))
        context = {
            "briques" : Brique.objects.filter(deleted = False, active = True),
            "types" : TypePerte.objects.filter(deleted = False),
            "pertes" : pertes,
        }
        return render(request, "production/pages/perte_brique.html", context)



def perte_ressource(request):
    if request.method == "GET":
        debut = datetime.date.fromisoformat(request.session["date1"])
        fin = datetime.date.fromisoformat(request.session["date2"]) + datetime.timedelta(days= 1)

        pertes = PerteRessource.objects.filter(deleted = False, agence = request.agence, created_at__range = (debut, fin))
        context = {
            "ressources" : Ressource.objects.filter(deleted = False, active = True),
            "types" : TypePerte.objects.filter(deleted = False),
            "pertes" : pertes,
        }
        return render(request, "production/pages/perte_ressource.html", context)







def rapport_production(request):
    if request.method == "GET":

        debut = datetime.date.fromisoformat(request.session["date1"])
        fin = datetime.date.fromisoformat(request.session["date2"]) 
        veille = debut - datetime.timedelta(days=1)
        lendemain = fin + datetime.timedelta(days=1)

        briques = {}
        for brique in Brique.objects.filter(active = True, deleted = False):
            data = {
                "veille"    : brique.stock(request.agence, veille),
                "stock"     : brique.stock(request.agence, fin), 
                "production": brique.production(request.agence, debut, fin), 
                "achat"     : brique.achat(request.agence, debut, fin), 
                "livraison": brique.livraison(request.agence, debut, fin), 
                "perteR"    : brique.perte_rangement(request.agence, debut, fin), 
                "perteL"    : brique.perte_livraison(request.agence, debut, fin), 
                "perteA"    : brique.perte_autre(request.agence, debut, fin), 
            }
            data["pct"] = 0;
            if data["production"] + data["achat"] > 0:
                data["pct"] = (brique.perte(request.agence, debut, fin) / (data["production"] + data["achat"])) * 100
            briques[brique] = data


        ressources = {}
        for ressource in Ressource.objects.filter(active = True, deleted = False):
            data = {
                "stock"    : ressource.stock(request.agence, fin), 
                "achat"    : ressource.achat(request.agence, debut, fin), 
                "consommee": ressource.consommation(request.agence, debut, fin), 
                "perte"    : ressource.perte(request.agence, debut, fin), 
            }
            ressources[ressource] = data

        cout_production = cout_rangement = cout_livraison =0
        for prod in Production.objects.filter(deleted = False, created_at__range = (debut, lendemain)):
            cout_production += prod.montant_production
            cout_rangement += prod.montant_rangement
            cout_livraison += prod.montant_livraison

        tricycle = Tricycle.objects.filter(deleted = False, created_at__range = (debut, lendemain)).aggregate(Sum("montant"))

        context = {
            "debut" : debut,
            "fin":fin,
            "veille":veille,
            "briques" : briques,
            "ressources" : ressources,

            "cout_production" : cout_production,
            "cout_rangement" : cout_rangement,
            "cout_livraison" : cout_livraison,
            "cout_tricycle" : tricycle["montant__sum"] or 0,
        }
        return render(request, "rapports/pages/production.html", context)

