import datetime
from django.shortcuts import get_object_or_404, render
from approvisionnementApp.models import AchatStock, Approvisionnement
from commandeApp.models import Conversion, GroupeCommande, PrixZoneLivraison, Commande, ZoneLivraison
from django.db.models import Sum
from coreApp.models import Etat
from livraisonApp.models import Livraison, Tricycle
from productionApp.models import Brique, Production, Ressource
from organisationApp.models import Employe
# Create your views here.

def rapport_du_jour(request, year, month, day):
    if request.method == "GET":
        date = datetime.date(year, month, day)
        veille = date - datetime.timedelta(days=1)

        commandes = {}
        for item in Commande.objects.filter(deleted = False, created_at__date = date):
            data = {}
            for ligne in item.commande_ligne.all():
                data[ligne.brique] = ligne.quantite
            commandes[item] = data

        livraisons = {}
        for item in Livraison.objects.filter(deleted = False, created_at__date = date).exclude(etat__etiquette = Etat.ANNULE):
            data = {}
            for ligne in item.livraison_ligne.all():
                data[ligne.brique] = ligne.quantite
            livraisons[item] = data

        appros = {}
        for item in Approvisionnement.objects.filter(deleted = False, created_at__date = date).exclude(etat__etiquette = Etat.ANNULE):
            data = {}
            for ligne in item.approvisionnement_ligne.all():
                data[ligne.ressource] = ligne.quantite
            appros[item] = data

        achats = {}
        for item in AchatStock.objects.filter(deleted = False, created_at__date = date).exclude(etat__etiquette = Etat.ANNULE):
            data = {}
            for ligne in item.achatstock_ligne.all():
                data[ligne.ressource] = ligne.quantite
            achats[item] = data


        production = {}
        prod = Production.objects.filter(date = date).first()
        if prod is not None:
            data = {}
            for ligne in prod.production_ligne.all():
                data[ligne.brique] = ligne.quantite
            production[prod] = data

        context = {
            "date" : date,
            "briques" : Brique.objects.filter(active = True, deleted = False),
            "ressources" : Ressource.objects.filter(active = True, deleted = False),
            'commandes' : commandes,
            'livraisons' : livraisons,
            'appros' : appros,
            'achats' : achats,
            "production" :production,
            'employes' : Employe.objects.filter(deleted = False, last_login__date = date),

            "entree_du_jour" : request.agence_compte.total_entree(date, date),
            "depense_du_jour" : request.agence_compte.total_sortie(date, date),
            "solde_ouverture" : request.agence_compte.solde_actuel(veille),
            "solde_fermeture" : request.agence_compte.solde_actuel(date),
        }
        return render(request, "rapports/pages/rapport_du_jour.html", context)






def production(request, id):
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

