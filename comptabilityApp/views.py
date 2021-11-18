from django.shortcuts import render
from approvisionnementApp.models import Fournisseur
from comptabilityApp.models import ReglementCommande
from clientApp.models import Client
from coreApp.models import Etat
from .models import CategoryOperation, Compte, Mouvement, ModePayement, TypeMouvement, TypeOperationCaisse
from commandeApp.models import Commande
import datetime
# Create your views here.

def caisse(request):
    if request.method == "GET":
        debut = datetime.date.fromisoformat(request.session["date1"])
        fin = datetime.date.fromisoformat(request.session["date2"])
        
        demain = request.now + datetime.timedelta(days= 1)
        lendemain = fin + datetime.timedelta(days= 1)

        datas = {}
        report = test = request.agence_compte.solde_actuel(debut)
        for mouvement in Mouvement.objects.filter(deleted=False, compte__agence = request.agence, created_at__range = (debut, lendemain)).exclude(mode__etiquette = ModePayement.PRELEVEMENT):
            test = (test - mouvement.montant) if mouvement.type.etiquette == TypeMouvement.RETRAIT else (test + mouvement.montant) 
            datas[mouvement] = test

        tableaux = request.agence_compte.stats(debut, fin)
        context = {
            "dette_clients" : Client.dette_clients(request.agence),
            "dette_fournisseurs" : Fournisseur.dette_fournisseurs(request.agence),
            "chiffre_affaire":Commande.chiffre_affaire(request.agence),

            "entree_du_jour" :request.agence_compte.total_entree(request.now.date(), demain),
            "depense_du_jour" : request.agence_compte.total_sortie(request.now.date(), demain),
            "solde_actuel" : request.agence_compte.solde_actuel(),
            "reglement_client" : ReglementCommande.total(request.agence, debut, lendemain),

            "attentes":Mouvement.objects.filter(deleted=False, compte__agence = request.agence, etat__etiquette = Etat.EN_COURS, created_at__range = (debut, lendemain)).exclude(mode__etiquette = ModePayement.PRELEVEMENT,),
            "mouvements":datas,
            "report":report,
            "total_entree" : request.agence_compte.total_entree(debut, lendemain),
            "total_depense" : request.agence_compte.total_sortie(debut, lendemain),
            "solde_a_la_date" : request.agence_compte.solde_actuel(lendemain),

            "categories_entrees" : CategoryOperation.objects.filter(deleted = False, type__etiquette = TypeOperationCaisse.DEPOT),
            "categories_depenses" : CategoryOperation.objects.filter(deleted = False, type__etiquette = TypeOperationCaisse.RETRAIT),
            "modes": ModePayement.objects.filter(deleted = False),
            "comptes": Compte.objects.filter(deleted = False).exclude(pk = request.agence_compte.id),

            "debut": debut,
            "fin": datetime.date.fromisoformat(request.session["date2"]),
            "tableaux" : tableaux,
            "stat" : tableaux[0],
        }
        return render(request, "tresorerie/pages/caisse.html", context)