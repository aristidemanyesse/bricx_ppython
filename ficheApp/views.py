import datetime
from django.shortcuts import get_object_or_404, render
from approvisionnementApp.models import AchatStock, Approvisionnement
from commandeApp.models import Conversion, GroupeCommande, PrixZoneLivraison, Commande, ZoneLivraison
from django.db.models import Sum
from comptabilityApp.models import ModePayement, Mouvement, TypeMouvement
from coreApp.models import Etat
from livraisonApp.models import Livraison, Tricycle
from productionApp.models import Brique, Production, Ressource
from organisationApp.models import Employe
# Create your views here.

def rapport_du_jour(request, year, month, day):
    if request.method == "GET":
        date = datetime.date(year, month, day)
        veille = date - datetime.timedelta(days=1)
        demain = date + datetime.timedelta(days=1)

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

        datas = {}
        report = test = request.agence_compte.solde_actuel(veille)
        for mouvement in Mouvement.objects.filter(deleted=False, compte__agence = request.agence, created_at__range = (date, demain)).exclude(mode__etiquette = ModePayement.PRELEVEMENT):
            test = (test - mouvement.montant) if mouvement.type.etiquette == TypeMouvement.RETRAIT else (test + mouvement.montant) 
            datas[mouvement] = test
            
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

            "mouvements":datas,
            "report":report,
            "total_entree" : request.agence_compte.total_entree(date, date),
            "total_depense" : request.agence_compte.total_sortie(date, date),
            "solde_a_la_date" : request.agence_compte.solde_actuel(date),
        }
        return render(request, "rapports/pages/rapport_du_jour.html", context)


