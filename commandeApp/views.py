from django.shortcuts import render
from comptabilityApp.models import ModePayement
from productionApp.models import Brique
from commandeApp.models import Conversion, ZoneLivraison, PrixZoneLivraison
from commandeApp.models import GroupeCommande
from coreApp.models import Etat
import datetime
# Create your views here.


def commandes(request):
    datas = []
    for groupe in GroupeCommande.objects.filter(etat__etiquette = Etat.EN_COURS):

        commandes = groupe.commande_groupecommande.filter(deleted = False)
        livraisons = groupe.groupecommande_livraison.filter(deleted = False)

        mylist = []
        mylist.extend(commandes)
        mylist.extend(livraisons)
        mylist.sort(key=lambda x: x.created_at)
        datas.append({
            "groupe":groupe,
            "commandes": commandes,
            "livraisons": livraisons,
            "livraisons_encours": groupe.groupecommande_livraison.filter(deleted = False, etat__etiquette = Etat.EN_COURS),
            "sort_lignes": mylist,
            "briques" : groupe.all_briques()

        })
        
    context = {
        "datas" : datas,
        "briques" : Brique.objects.filter(active = True, deleted = False),
        'commandes' : GroupeCommande.objects.filter(etat__etiquette = Etat.EN_COURS),

        "modepayements": ModePayement.objects.filter(deleted = False),
        "zonelivraisons": ZoneLivraison.objects.filter(deleted = False),
    }
    return render(request, "commande/pages/commandes.html", context)




def commandes1(request):
    context = {}
    return render(request, "commande/pages/commandes1.html", context)



def conversions(request):
    context = {
        "conversions" : Conversion.objects.filter(deleted= False, created_at__range=(request.session["date1"], request.session["date2"]))
    }
    return render(request, "commande/pages/conversions.html", context)




def prixparzone(request):
    if request.method == "GET":
        context = {
            "briques" : Brique.objects.filter(active = True),
            "zones" : ZoneLivraison.objects.filter(),
            "prixparzones" : PrixZoneLivraison.objects.filter()
        }
        return render(request, "commande/pages/prixparzone.html", context)



