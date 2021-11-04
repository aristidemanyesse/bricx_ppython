from django.contrib.auth.models import User, Permission
from coreApp.models import BaseModel, MyCodeException


def run():
    User.objects.create_superuser(
        username = "admin",
        email = "info@devaris21.com",
        password="Samageste1",
        first_name = "Super",
        last_name = "Administrateur"
    )
    
    print("Initialisation du module d'Authentification")