from django.shortcuts import get_object_or_404, render
from approvisionnementApp.models import AchatStock, Approvisionnement
from commandeApp.models import Conversion, PrixZoneLivraison, Commande, ZoneLivraison
from comptabilityApp.models import Mouvement
from livraisonApp.models import Livraison
from productionApp.models import Production

# Create your views here.
def prixparzone(request, id):
    if request.method == "GET":
        zone = get_object_or_404(ZoneLivraison, pk = id)
        context = {
                "zone" : zone,
            }
        return render(request, "fiches/pages/prixparzone.html", context)



def commande(request, id):
    if request.method == "GET":
        commande = get_object_or_404(Commande, pk = id)
        context = {
                "commande" : commande,
                "reglement" : commande.commande_reglement.filter(deleted = False).first(),
            }
        return render(request, "fiches/pages/commande.html", context)



def livraison(request, id):
    if request.method == "GET":
        livraison = get_object_or_404(Livraison, pk = id)
        context = {
                "livraison" : livraison,
            }
        return render(request, "fiches/pages/livraison.html", context)



def conversion(request, id):
    if request.method == "GET":
        conversion = get_object_or_404(Conversion, pk = id)
        context = {
                "conversion" : conversion,
            }
        return render(request, "fiches/pages/conversion.html", context)



def production(request, id):
    if request.method == "GET":
        production = get_object_or_404(Production, pk = id)
        total = 0
        for ligne in production.production_ligneconsommation.all() :
            total += ligne.ressource.estimation(production.agence) * ligne.quantite

        context = {
                "total" : total,
                "production" : production,
            }
        return render(request, "fiches/pages/production.html", context)


def approvisionnement(request, id):
    if request.method == "GET":
        approvisionnement = get_object_or_404(Approvisionnement, pk = id)
        context = {
                "appro" : approvisionnement,
                "reglement" : approvisionnement.approvisionnement_reglement.filter(deleted = False).first(),
            }
        return render(request, "fiches/pages/approvisionnement.html", context)


def achatstock(request, id):
    if request.method == "GET":
        achatstock = get_object_or_404(AchatStock, pk = id)
        context = {
                "achat" : achatstock,
            }
        return render(request, "fiches/pages/achatstock.html", context)




def boncaisse(request, id):
    if request.method == "GET":
        mouvement = get_object_or_404(Mouvement, pk = id)
        context = {
                "mouvement" : mouvement,
            }
        return render(request, "fiches/pages/boncaisse.html", context)