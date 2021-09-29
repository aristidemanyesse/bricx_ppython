from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from organisationApp.models import Employe, Agence
from commandeApp.models import Client
from paramApp.models import Params
from productionApp.models import Brique

# Create your views here.
@login_required
def home(request):
    datas = {
        "users" : Employe.objects.all().count(),
        "clients" : Client.objects.all().count(),
        "briques" : Brique.objects.filter(active = True).count(),
        "agences" : Agence.objects.all().count(),
    }
    return render(request, "core/pages/home.html", datas)