

from authApp.models import AccesAgence
from organisationApp.models import Agence, Employe


def run():

    agence = Agence.objects.create(
        name = "La nouvelle fabrique",
        lieu = "...",
        protected = True
    )

    employe = Employe.objects.create(
        first_name = "Super",
        last_name = "administrateur",
        email = "test@email.com",
        username = "bricx",
        password = "bricx",
        agence = agence,
        protected = True
    )

    AccesAgence.objects.create(
        employe = employe,
        agence = agence,
        protected = True
    )
    
    print("bootstrap.py de orga")