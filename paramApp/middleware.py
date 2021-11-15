from django.contrib.auth.models import Permission
from approvisionnementApp.models import AchatStock, Approvisionnement
from commandeApp.models import GroupeCommande
from livraisonApp.models import Livraison, Tricycle
from coreApp.models import Etat
from coreApp import tools
from paramApp.models import MyApp, MyCompte
from comptabilityApp.models import ModePayement, TypeMouvement
import datetime, uuid
from django.shortcuts import redirect


class InjectMyAppDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        if "date1" not in request.session:
            request.session["date1"] = str((datetime.datetime.now() - datetime.timedelta(days=3)).date())
            request.session["date2"] = str((datetime.datetime.now()).date())
            
        request.date1 = datetime.date.fromisoformat(request.session["date1"])
        request.date2 = datetime.date.fromisoformat(request.session["date2"])
            
        if not request.path_info.startswith('/admin/'):
    
            request.agence = None
            if request.user.is_authenticated:
                request.agence = request.user.employe.agence
                compte = request.agence.agence_compte.all().first()
                request.agence_compte = compte

                request.commandes = GroupeCommande.objects.filter(agence = request.agence, etat__etiquette = Etat.EN_COURS)
                request.livraisons = Livraison.objects.filter(groupecommande__agence = request.agence, etat__etiquette = Etat.EN_COURS)
                request.tricycles = Tricycle.objects.filter(livraison__groupecommande__agence = request.agence, deleted = False)
                request.appros = Approvisionnement.objects.filter(agence = request.agence, deleted = False, etat__etiquette = Etat.EN_COURS)
                request.achats = AchatStock.objects.filter(agence = request.agence, deleted = False, etat__etiquette = Etat.EN_COURS)


