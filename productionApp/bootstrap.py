

from productionApp.models import Brique, Ressource, TypePerte


def run():

    TypePerte.objects.create(
        name = "Perte au chargement",
        etiquette = TypePerte.CHARGEMENT,
        protected = True
    )
    TypePerte.objects.create(
        name = "Perte au dechargement",
        etiquette = TypePerte.DECHARGEMENT,
        protected = True
    )
    TypePerte.objects.create(
        name = "Surplus de la production",
        protected = True
    )
    TypePerte.objects.create(
        name = "Dégats",
        protected = True
    )
    TypePerte.objects.create(
        name = "Vol",
        protected = True
    )


    Brique.objects.create(
        name = "AP 15",
        comment = "Agglos pleines 15",
        alert_stock = 10,
        protected = True
    )


    Ressource.objects.create(
        name = "Ciment",
        unite = "Chrgs",
        protected = True
    )

    print("Initialisation du module de Production")