from django.shortcuts import get_object_or_404, render
from commandeApp.models import Conversion, PrixZoneLivraison, Commande, ZoneLivraison
from comptabilityApp.models import Mouvement
from livraisonApp.models import Livraison

# Create your views here.
def prixparzone(request, id):
    if request.method == "GET":
        zone = get_object_or_404(ZoneLivraison, pk = id)
        context = {
                "zone" : zone,
                "prixparzones" : zone.zone_prix.filter(),
            }
        return render(request, "fiches/pages/prixparzone.html", context)



def commande(request, id):
    if request.method == "GET":
        zone = get_object_or_404(Commande, pk = id)
        context = {
                "zone" : zone,
            }
        return render(request, "fiches/pages/commande.html", context)



def livraison(request, id):
    if request.method == "GET":
        livraison = get_object_or_404(Livraison, pk = id)
        context = {
                "livraison" : livraison,
            }
        return render(request, "fiches/pages/livraison.html", context)



def tricycle(request, id):
    if request.method == "GET":
        tricycle = get_object_or_404(Livraison, pk = id)
        context = {
                "tricycle" : tricycle,
            }
        return render(request, "fiches/pages/tricycle.html", context)


def conversion(request, id):
    if request.method == "GET":
        converson = get_object_or_404(Conversion, pk = id)
        context = {
                "conversion" : conversion,
            }
        return render(request, "fiches/pages/conversion.html", context)


def production(request, id):
    if request.method == "GET":
        converson = get_object_or_404(Production, pk = id)
        context = {
                "production" : production,
            }
        return render(request, "fiches/pages/production.html", context)


def boncaisse(request, id):
    if request.method == "GET":
        zone = get_object_or_404(Mouvement, pk = id)
        context = {
                "zone" : zone,
            }
        return render(request, "fiches/pages/boncaisse.html", context)