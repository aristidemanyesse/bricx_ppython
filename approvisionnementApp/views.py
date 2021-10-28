from django.shortcuts import render
from commandeApp.models import GroupeCommande, ZoneLivraison
from livraisonApp.models import Chauffeur, ModeLivraison, Vehicule
from productionApp.models import Brique, Ressource
from comptabilityApp.models import ModePayement
from coreApp.models import Etat
from .models import AchatStock, Approvisionnement, Fournisseur
from django.shortcuts import get_object_or_404
import datetime
# Create your views here.


def fournisseurs(request):
    if request.method == "GET":
        date = datetime.datetime.now() - datetime.timedelta(days=7)
        ctx = {
            "fournisseurs" : Fournisseur.objects.filter(agence = request.agence),
        }
        return render(request, "appros/pages/fournisseurs.html", ctx)
        



def fournisseur(request, fournisseur_id):
    if request.method == "GET":
        fournisseur = get_object_or_404(Fournisseur, pk = fournisseur_id)
        request.session["fournisseur_id"] = str(fournisseur.id)

        datas = fournisseur.fournisseur_approvisionnement.filter(deleted = False)
        
        context = {
            'fournisseur' : fournisseur,
            'fournisseurs' : Fournisseur.objects.filter(deleted=False, agence = request.agence),
            "appros" : datas,
            "ressources" : Ressource.objects.filter(active = True, deleted = False),
            "modepayements": ModePayement.objects.filter(deleted = False),

        }
        return render(request, "appros/pages/fournisseur.html", context)




def approvisionnements(request):
    context = {
        'appros' : Approvisionnement.objects.filter(deleted = False),
        'fournisseurs' : Fournisseur.objects.filter(deleted = False, agence = request.agence),
        "ressources" : Ressource.objects.filter(active = True, deleted = False),
        "modepayements": ModePayement.objects.filter(deleted = False),
    }
    return render(request, "appros/pages/approvisionnements.html", context)



def achatstock(request):
    context = {
        'achats' : AchatStock.objects.filter(deleted = False),
        'fournisseurs' : Fournisseur.objects.filter(deleted = False, agence = request.agence),
        "briques" : Brique.objects.filter(active = True, deleted = False),
        "modepayements": ModePayement.objects.filter(deleted = False),
    }
    return render(request, "appros/pages/achatstock.html", context)

