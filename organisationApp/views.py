from django.shortcuts import render
from django.http import  JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from django.shortcuts import render
from comptabilityApp.models import Mouvement
from organisationApp.models import Agence, Employe
from authApp.models import AccesAgence
from productionApp.models import Brique, Ressource
from clientApp.models import Client
from django.contrib.auth import authenticate
# Create your views here.



def home(request):
    datas = {
        "nb_users" : Employe.objects.all().count(),
        "nb_clients" : Client.objects.all().count(),
        "nb_briques" : Brique.objects.filter(active = True).count(),
        "nb_agences" : Agence.objects.all().count(),
    }
    return render(request, "master/pages/home.html", datas)



def dashboard_boutique(request):
    datas = {}
    briques = Brique.objects.filter(active = True, deleted = False)
    for brique in briques:
        data = {
            "attente" : int(brique.attente(request.agence)),
            "livrable" : int(brique.livrable(request.agence)),
            "commande" : int(brique.commande(request.agence)),
        }
        datas[brique] = data

    

    context = {
        "datas" : datas,
        "dette_clients" : Client.dette_clients(request.agence),
        "entree_du_jour" :request.agence_compte.total_entree(request.now.date(), request.now.date()),
        "depense_du_jour" : request.agence_compte.total_sortie(request.now.date(), request.now.date()),
        "solde_actuel" : request.agence_compte.solde_actuel(),
        "rupture_stock_brique" : Brique.en_rupture(request.agence)
    }

    return render(request, "boutique/pages/dashboard.html", context)




def dashboard_fabrique(request):
    datas = {}
    datas_ressources = {}
    for brique in Brique.objects.filter(active = True, deleted = False):
        data = {
            "attente" : int(brique.attente(request.agence)),
            "livrable" : int(brique.livrable(request.agence)),
            "commande" : int(brique.commande(request.agence)),
        }
        datas[brique] = data



    for ressource in Ressource.objects.filter(active = True, deleted = False):
        data = {
            "stock" : ressource.stock(request.agence),
        }
        datas_ressources[ressource] = data



    context = {
        "datas" : datas,
        "datas_ressources" : datas_ressources
    }

    return render(request, "fabrique/pages/dashboard.html", context)

