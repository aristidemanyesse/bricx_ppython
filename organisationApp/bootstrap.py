

from django.contrib.auth.models import Permission
from authApp.models import AccesAgence
from organisationApp.models import Agence, Employe


def run():

    agence = Agence.objects.create(
        name = "La nouvelle fabrique",
        lieu = "...",
        protected = True
    )

    employe = Employe.objects.create(
        first_name = "Super administrateur",
        email = "test@email.com",
        username = "bricx",
        brut = "bricx",
        agence = agence,
        protected = True
    )
    employe.user_permissions.set(Permission.objects.filter(name__contains = "~"))

    
    print("Initialisation du module d' Organisation")