from .models import ZoneLivraison
from organisationApp.models import Agence


def run():

    ZoneLivraison.objects.create(
        name="Dans les alentours",
        agence=Agence.objects.filter(deleted=False).first(),
    )

    print("Initialisation du module de Commandes")
