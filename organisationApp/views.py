from django.shortcuts import render
from django.http import  JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from django.shortcuts import render
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



def boutique(request):
    agence = get_object_or_404(Agence, pk=request.agence.id)
    return render(request, "boutique/pages/dashboard.html")



def fabrique(request):
    agence = get_object_or_404(Agence, pk=request.agence.id)
    return render(request, "fabrique/pages/dashboard.html")


def dashboard(request):
    if request.method == "GET":
        agence = get_object_or_404(Agence, pk=request.agence.id)
        return render(request, "organisation/pages/dashboard.html")
