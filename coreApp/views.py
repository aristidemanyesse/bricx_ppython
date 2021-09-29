from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from organisationApp.models import Employe, Agence
from authApp.models import AccesAgence
from commandeApp.models import Client
from productionApp.models import Brique

# Create your views here.
@login_required
def home(request):
    agence = AccesAgence.objects.filter(employe = request.user).first()
    datas = {
        "nb_users" : Employe.objects.all().count(),
        "nb_clients" : Client.objects.all().count(),
        "nb_briques" : Brique.objects.filter(active = True).count(),
        "nb_agences" : Agence.objects.all().count(),
        "agence" : agence,
    }
    return render(request, "core/pages/home.html", datas)