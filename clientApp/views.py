from django.shortcuts import render
from commandeApp.models import GroupeCommande
from productionApp.models import Brique
from comptabilityApp.models import ModePayement
from coreApp.models import Etat
from .models import TypeClient, Client
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
        request.session["client_id"] = str(client.id)

        datas = []
        for groupe in client.get_groupecommandes():
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
                "sort_lignes": mylist
            })

        context = {
            'client' : client,
            'clients' : Client.objects.filter(agence = request.agence),
            'types' : TypeClient.objects.all(),
            "datas" : datas,
            "briques" : Brique.objects.filter(active = True, deleted = False),
            'commandes' : GroupeCommande.objects.filter(etat__etiquette = Etat.EN_COURS),

            "modepayements": ModePayement.objects.filter(deleted = False)
        }
        return render(request, "clients/pages/client.html", context)