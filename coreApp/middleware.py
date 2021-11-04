
import datetime
import uuid, pytz
from django.shortcuts import redirect
from django.utils.timezone import make_aware
from comptabilityApp.models import ModePayement, TypeMouvement
from coreApp import tools
from coreApp.models import Etat
from paramApp.models import MyApp, MyCompte


class LockoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response     

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.path_info.startswith('/admin/') and not request.path_info.startswith('/auth/'):
            if 'locked' in request.session:
                if request.session['locked'] :
                    return redirect("auth:locked")

            if not request.user.is_authenticated:
                return redirect("auth:login")



class  AccessCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response    

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.module_name = request.path_info.split("/")[1]
        try:
            test = uuid.UUID(request.path_info.split("/")[3], version=4)
        except:
            test = False
            
        if request.path_info.split("/")[3] != "" and not test:
            request.page_name = request.path_info.split("/")[3]
        else:
            request.page_name = request.path_info.split("/")[2] if request.path_info.split("/")[2] != "" else "dashboard_"+request.module_name

        request.societe = MyApp.objects.all().first()
        request.mycompte = MyCompte.objects.all().first()
        if not request.path_info.startswith('/admin/') and not request.path_info.startswith('/auth/expiration/') :
            request.now = datetime.datetime.now()
            request.etat = Etat
            request.modepayement = ModePayement
            request.typemouvement = TypeMouvement
            request.isferie = tools.is_ferie(request.now)
            request.uuid = uuid.uuid4()

            if not (request.mycompte.expiration >= make_aware(datetime.datetime.now())):
                return redirect("auth:expiration")
