from django.shortcuts import render
from productionApp.models import Brique
from commandeApp.models import ZoneLivraison, PrixZoneLivraison
from commandeApp.models import GroupeCommande
from coreApp.models import Etat
import datetime
# Create your views here.


def commandes(request):
    datas = []
    for groupe in GroupeCommande.objects.filter(etat__etiquette = Etat.EN_COURS):

        datas.append({
                "groupe":groupe,
                "commandes": groupe.commande_groupecommande.filter(etat__etiquette = Etat.EN_COURS),
                "livraisons": groupe.groupecommande_livraison.filter(etat__etiquette = Etat.EN_COURS),
                "briques" : groupe.all_briques()
            })
        
    context = {
        "datas" : datas,
        "briques" : Brique.objects.filter(active = True, deleted = False)
    }
    return render(request, "commande/pages/commandes.html", context)




def commandes1(request):
    context = {}
    return render(request, "commande/pages/commandes1.html", context)



def prixparzone(request):
    if request.method == "GET":
        context = {
            "briques" : Brique.objects.filter(active = True),
            "zones" : ZoneLivraison.objects.filter(),
            "prixparzones" : PrixZoneLivraison.objects.filter()
        }
        return render(request, "commande/pages/prixparzone.html", context)



