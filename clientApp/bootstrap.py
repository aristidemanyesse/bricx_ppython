
from clientApp.models import TypeClient


def run():
    TypeClient.objects.create(
        name = "Entreprise",
        etiquette = TypeClient.ENTREPRISE,
        protected = True
    )
    TypeClient.objects.create(
            name = "Particulier",
            etiquette = TypeClient.PARTICULIER,
            protected = True
    )

    print("bootstrap.py de client")