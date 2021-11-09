from django.shortcuts import render
from commandeApp.models import GroupeCommande, ZoneLivraison
from livraisonApp.models import Chauffeur, ModeLivraison, Vehicule
from productionApp.models import Brique
from comptabilityApp.models import CompteClient, ModePayement, Mouvement, ReglementCommande
from coreApp.models import Etat
from .models import TypeClient, Client
from django.shortcuts import get_object_or_404
import datetime
# Create your views here.


def clients(request):
    if request.method == "GET":
        GroupeCommande.maj_etat()
        date = datetime.datetime.now() - datetime.timedelta(days=7)
        ctx = {
            "clients" : Client.objects.filter(agence = request.agence),
            "clients_semaine" : Client.objects.filter(agence = request.agence, created_at__gte = date ),
            "types" : TypeClient.objects.filter(deleted = False)
        }
        return render(request, "clients/pages/clients.html", ctx)
        



def client(request, client_id):
    try:
        del request.session["groupecommande_id"]
    except Exception as e:
        print("view de client :", e)

    if request.method == "GET":
        client = get_object_or_404(Client, pk = client_id)
        request.session["client_id"] = str(client.id)

        datas = []
        for groupe in client.get_groupecommandes():
            commandes = groupe.commande_groupecommande.filter(deleted = False)
            livraisons = groupe.groupecommande_livraison.filter(deleted = False).exclude(etat__etiquette = Etat.ANNULE)

            for commande in commandes:
                commande.tipe = "commande"
            for livraison in livraisons:
                livraison.tipe = "livraison"

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

        items = []
        for item in ReglementCommande.objects.filter(commande__groupecommande__client = client, deleted = False):
            items.append(item.mouvement)
        for item in CompteClient.objects.filter(client = client, deleted = False):
            if item.mouvement not in items:
                items.append(item.mouvement)
        items.sort(key=lambda x: x.created_at)

        context = {
            'client' : client,
            'clients' : Client.objects.filter(agence = request.agence),
            'types' : TypeClient.objects.filter(deleted = False),
            "datas" : datas,
            "briques" : Brique.objects.filter(active = True, deleted = False),
            'commandes' : GroupeCommande.objects.filter(etat__etiquette = Etat.EN_COURS),

            "chauffeurs": Chauffeur.objects.filter(deleted = False, agence = request.agence),
            "vehicules": Vehicule.objects.filter(deleted = False, agence = request.agence),
            "modepayements": ModePayement.objects.filter(deleted = False),
            "zonelivraisons": ZoneLivraison.objects.filter(deleted = False, agence = request.agence),
            "modelivraisons": ModeLivraison.objects.filter(deleted = False),
            "mouvements": items,

        }
        return render(request, "clients/pages/client.html", context)