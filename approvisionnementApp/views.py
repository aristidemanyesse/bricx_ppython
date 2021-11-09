from django.shortcuts import render
from commandeApp.models import GroupeCommande, ZoneLivraison
from livraisonApp.models import Chauffeur, ModeLivraison, Vehicule
from productionApp.models import Brique, Ressource
from comptabilityApp.models import CompteFournisseur, ModePayement, ReglementApprovisionnement
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
        
        items = []
        for item in ReglementApprovisionnement.objects.filter(approvisionnement__fournisseur = fournisseur, deleted = False):
            items.append(item.mouvement)
        for item in CompteFournisseur.objects.filter(fournisseur = fournisseur, deleted = False):
            if item.mouvement not in items:
                items.append(item.mouvement)
        items.sort(key=lambda x: x.created_at)

        context = {
            'fournisseur' : fournisseur,
            'fournisseurs' : Fournisseur.objects.filter(deleted=False, agence = request.agence),
            "appros" : datas,
            "ressources" : Ressource.objects.filter(active = True, deleted = False),
            "modepayements": ModePayement.objects.filter(deleted = False),
            "mouvements": items,

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

