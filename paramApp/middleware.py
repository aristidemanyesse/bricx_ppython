from paramApp.models import MyApp, MyCompte
from django.contrib.auth.models import User, AnonymousUser
import datetime, uuid

class InjectMyAppDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
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

        response = self.get_response(request)
        return response     