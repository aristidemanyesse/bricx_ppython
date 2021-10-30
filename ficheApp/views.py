import datetime
from django.shortcuts import get_object_or_404, render
from approvisionnementApp.models import AchatStock, Approvisionnement
from commandeApp.models import Conversion, GroupeCommande, PrixZoneLivraison, Commande, ZoneLivraison
from comptabilityApp.models import Mouvement
from coreApp.models import Etat
from livraisonApp.models import Livraison
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
        converson = get_object_or_404(Production, pk = id)
        context = {
                "production" : production,
            }
        return render(request, "fiches/pages/production.html", context)

