from commandeApp.models import GroupeCommande
from livraisonApp.models import Livraison, Tricycle
from coreApp.models import Etat
from paramApp.models import MyApp, MyCompte
import datetime, uuid
from django.shortcuts import redirect


class InjectMyAppDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.etat = Etat
        if "date1" not in request.session:
            request.session["date1"] = str((datetime.datetime.now() - datetime.timedelta(days=2)).date())
            request.session["date2"] = str((datetime.datetime.now() + datetime.timedelta(days=1)).date())

        if not request.path_info.startswith('/admin/'):

            request.uuid = uuid.uuid4()
            request.societe = MyApp.objects.all().first()
            request.mycompte = MyCompte.objects.all().first()
            request.now = datetime.datetime.now()

            if request.user.is_authenticated:
                access = request.user.employe.employe_acces.first()
                request.agence = None
                if access is not None:
                    request.agence = access.agence

                    request.commandes = GroupeCommande.objects.filter(agence = request.agence, etat__etiquette = Etat.EN_COURS)
                    request.livraisons = Livraison.objects.filter(groupecommande__agence = request.agence, etat__etiquette = Etat.EN_COURS)
                    request.tricycles = Tricycle.objects.filter(livraison__groupecommande__agence = request.agence, etat__etiquette = Etat.EN_COURS)




class LockoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        if not request.path_info.startswith('/admin/') or not request.path_info.startswith('/auth/'):
            if 'locked' in request.session:
                if request.session['locked'] :
                    redirect("auth:login")

        response = self.get_response(request)
        return response     