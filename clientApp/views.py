from django.shortcuts import render
from commandeApp.models import GroupeCommande
from coreApp.models import Etat
from clientApp.models import TypeClient, Client
from django.shortcuts import get_object_or_404
import uuid
# Create your views here.


def clients(request):
    if request.method == "GET":
        ctx = {
            "clients" : Client.objects.filter(agence = request.agence),
            "types" : TypeClient.objects.all()
        }
        return render(request, "clients/pages/clients.html", ctx)
        

def client(request, client_id):
    if request.method == "GET":
        client = get_object_or_404(Client, pk = client_id)
        datas = {
            'client' : client,
            'clients' : Client.objects.filter(agence = request.agence),
            'types' : TypeClient.objects.all(),
            'commandes' : GroupeCommande.objects.filter(etat = Etat.ENCOURS)
        }
        return render(request, "clients/pages/client.html", datas)