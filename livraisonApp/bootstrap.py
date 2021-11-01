

from livraisonApp.models import ModeLivraison


def run():

    ModeLivraison.objects.create(
        name = "Avec nos véhicules et nos manoeuvres",
        etiquette = ModeLivraison.DEFAUT,
        protected = True
    )
    ModeLivraison.objects.create(
        name = "Livraison avec un ttricycle",
        etiquette = ModeLivraison.TRICYCLE,
        protected = True
    )
    ModeLivraison.objects.create(
        name = "Par les moyens du client",
        etiquette = ModeLivraison.CLIENT,
        protected = True
    )



    print("Initialisation du module de Livraison")