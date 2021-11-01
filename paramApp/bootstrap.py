
import uuid, datetime
from paramApp.models import MyApp, MyCompte


def run():

    MyCompte.objects.create(
        identifiant = uuid.uuid4(),
        expiration = datetime.datetime.now() + datetime.timedelta(days=30),
        tentative = 3
    )

    MyApp.objects.create(
        socialreason = "Devaris 21",
        email = "info@devaris21.pro",
        devise = "Fcfa"
    )
    
    print("Initialisation du module d'Adminnistration")