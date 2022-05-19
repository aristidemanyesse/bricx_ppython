

from coreApp.models import Etat


def run():

    Etat.objects.create(
        name = "Terminé",
        classe = "success",
        etiquette = Etat.TERMINE
    )
    Etat.objects.create(
        name = "En cours",
        classe = "default",
        etiquette = Etat.EN_COURS
    )
    Etat.objects.create(
        name = "Annulé",
        classe = "danger",
        etiquette = Etat.ANNULE
    )



    print("Initialisation du module de Core")