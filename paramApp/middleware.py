from paramApp.models import Params, MyCompte
from django.contrib.auth.models import User, AnonymousUser


class InjectParamsDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):

        request.societe = Params.objects.all().first()
        request.mycompte = MyCompte.objects.all().first()
        if request.user is not AnonymousUser:
            request.user = request.user

        response = self.get_response(request)
        return response