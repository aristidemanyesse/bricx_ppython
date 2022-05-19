from django.shortcuts import render
import datetime
from comptabilityApp.models import ModePayement

from coreApp.models import Etat
from livraisonApp.models import Livraison, ModeLivraison, Tricycle
# Create your views here.


def livraisons(request):
    if request.method == "GET":
        request.modelivraison = ModeLivraison
        debut = datetime.date.fromisoformat(request.session["date1"])
        fin = datetime.date.fromisoformat(request.session["date2"]) + datetime.timedelta(days= 1) 

        context = {
            "debut" : debut,
            "fin":fin,
            "livraisons" : Livraison.objects.filter(deleted = False, created_at__range = (debut, fin))
        }
        return render(request, "livraison/pages/livraisons.html", context)



def tricycles(request):
    if request.method == "GET":
        request.modelivraison = ModeLivraison
        debut = datetime.date.fromisoformat(request.session["date1"])
        fin = datetime.date.fromisoformat(request.session["date2"]) + datetime.timedelta(days= 1) 

        context = {
            "debut" : debut,
            "fin":fin,
            "modes": ModePayement.objects.filter(deleted = False),
            "tricycles" : Tricycle.objects.filter(deleted = False, created_at__range = (debut, fin)),
        }
        return render(request, "livraison/pages/tricycles.html", context)