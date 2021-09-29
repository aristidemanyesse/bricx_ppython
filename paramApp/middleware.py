from paramApp.models import MyApp, MyCompte
from django.contrib.auth.models import User, AnonymousUser
import datetime

class InjectMyAppDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):

        request.societe = MyApp.objects.all().first()
        request.mycompte = MyCompte.objects.all().first()
        request.now = datetime.datetime.now()
        if request.user is not AnonymousUser:
            request.user = request.user

        response = self.get_response(request)
        return response