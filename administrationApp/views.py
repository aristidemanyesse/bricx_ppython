from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404, render

from commandeApp.models import ZoneLivraison, PrixZoneLivraison
from comptabilityApp.models import CategoryOperation, Compte, TypeOperationCaisse
from organisationApp.models import Agence, Employe
from paramApp.models import MyCompte
from productionApp.models import Brique, PayeBrique, PayeBriqueFerie, Ressource
from livraisonApp.models import Vehicule, Chauffeur
# Create your views here.


def dashboard(request):
    if request.method == "GET":
        context = {}
        return render(request, "admin/pages/dashboard.html", context)
        pass




def general(request):
    if request.method == "GET":
        context = {}
        return render(request, "admin/pages/general.html", context)


def roles(request):
    if request.method == "GET":
        datas={}
        for employe in Employe.objects.filter(deleted = False):
            datas[employe] = Permission.objects.filter(codename__in = employe.get_all_permissions()) 

        context = {
            "employes" : datas,
            "agences" : Agence.objects.filter(deleted = False),
            "permissions_on" : Permission.objects.filter(name__contains = "BRICX |")
        }
        return render(request, "admin/pages/roles.html", context)


def mycompte(request):
    if request.method == "GET":
        context = {
            "employes" : Employe.objects.filter(deleted = False),
            "agences" : Agence.objects.filter(deleted = False),
            "mycompte": MyCompte.objects.filter().first(),
        }
        return render(request, "admin/pages/mycompte.html", context)





def organisation(request):
    if request.method == "GET":

        context = {
            "agences" : Agence.objects.filter(deleted = False),
            "employes" : Employe.objects.filter(deleted = False),
            "organisation": MyCompte.objects.filter().first(),
        }
        return render(request, "admin/pages/organisation.html", context)



def production(request):
    if request.method == "GET":
        datas= {}
        for brique in Brique.objects.filter(deleted = False):
            exi = brique.brique_exigenceproduction.filter().first()
            data = {}
            for ressource in Ressource.objects.filter(deleted = False):
                item = ressource.ressource_exigenceligne.filter(exigence = exi).first()
                data[ressource] = item.quantite if item != None else 0

            datas[brique] = data

        context = {
            "briques" : datas,
            "ressources" : Ressource.objects.filter(deleted = False),
        }
        return render(request, "admin/pages/production.html", context)




def agence(request, id):
    if request.method == "GET":
        agence = get_object_or_404(Agence, pk = id)
        datas = {}
        for employe in Employe.objects.filter(deleted = False, agence = agence):
            perms_off = []
            perms = employe.user_permissions.filter()
            data = {}
            data["perms_on"] = perms 
            items = Permission.objects.filter(name__contains="BRICX")
            for p in items:
                if p not in perms: 
                    perms_off.append(p)

            data["perms_off"] = perms_off
            datas[employe] = data

        context = {
            "agence" : agence,
            "agences" : Agence.objects.filter(deleted = False),
            "compte" : agence.agence_compte.all().first(),
            "prixparzones": PrixZoneLivraison.objects.filter(deleted = False),
            "vehicules" : Vehicule.objects.filter(deleted = False, agence = agence),
            "chauffeurs" : Chauffeur.objects.filter(deleted = False, agence = agence),
            "briques" : Brique.objects.filter(deleted = False),
            "zones" : ZoneLivraison.objects.filter(agence = agence),
            "employes" : datas
        }
        return render(request, "admin/pages/agence.html", context)



def prices(request):
    if request.method == "GET":
        datas={}
        for agence in Agence.objects.filter(deleted = False):
            data = {}
            data["zones"] = ZoneLivraison.objects.filter(deleted = False, agence = agence)
            datas[agence] = data

        context = {
            "agences" : datas,
            "briques" : Brique.objects.filter(deleted = False),
            "prixparzones": PrixZoneLivraison.objects.filter(deleted = False),
            "payes": PayeBrique.objects.filter(deleted = False),
            "payeferies": PayeBriqueFerie.objects.filter(deleted = False),
        }
        return render(request, "admin/pages/prices.html", context)



def caisse(request):
    if request.method == "GET":
        context = {
            "entrees" : CategoryOperation.objects.filter(deleted = False, type__etiquette = TypeOperationCaisse.DEPOT),
            "depenses" : CategoryOperation.objects.filter(deleted = False, type__etiquette = TypeOperationCaisse.RETRAIT),
            "types" : TypeOperationCaisse.objects.filter(deleted = False),
            "comptes" : Compte.objects.filter(deleted = False),
        }
        return render(request, "admin/pages/caisse.html", context)
