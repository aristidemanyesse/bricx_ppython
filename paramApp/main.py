from clientApp.models import TypeClient


TypeClient.objects.create(
    name = "Entreprise",
    etiquette = TypeClient.ENTREPRISE
)
TypeClient.objects.create(
    name = "Particulier",
    etiquette = TypeClient.PARTICULIER
)



ETAT.objects.create(
    name = "Terminé",
    classe = "danger",
    etiquette = ETAT.TERMINE
)
ETAT.objects.create(
    name = "En cours",
    classe = "info",
    etiquette = ETAT.ENCOURS
)
ETAT.objects.create(
    name = "Annulé",
    classe = "success",
    etiquette = ETAT.ANNULE
)




TypeMouvement.objects.create(
    name = "Entrée",
    etiquette = TypeMouvement.DEPOT
)
TypeMouvement.objects.create(
    name = "Sortie",
    etiquette = TypeMouvement.RETRAIT
)


TypeOperationCaisse.objects.create(
    name = "Entrée",
    etiquette = TypeOperationCaisse.DEPOT
)
TypeOperationCaisse.objects.create(
    name = "Sortie",
    etiquette = TypeOperationCaisse.RETRAIT
)


MODEPAYEMENT.objects.create(
    name = "Prélèvement sur acompte",
    etat = Etat.objects.get(etiquette = ETAT.TERMINE),
    etiquette = MODEPAYEMENT.PRELEVEMENT
)
MODEPAYEMENT.objects.create(
    name = "En espèces",
    etat = Etat.objects.get(etiquette = ETAT.TERMINE),
    etiquette = MODEPAYEMENT.ESPECES
)
MODEPAYEMENT.objects.create(
    name = "Mobile Money",
    etat = Etat.objects.get(etiquette = ETAT.ENCOURS),
    etiquette = MODEPAYEMENT.MOBILE_MONEY
)
MODEPAYEMENT.objects.create(
    name = "Par chèque",
    etat = Etat.objects.get(etiquette = ETAT.ENCOURS),
    etiquette = MODEPAYEMENT.CHEQUE
)





CategorieOperation.objects.create(
    name = "Remboursement du client",
    etiquette = CategorieOperation.REFUND_CLIENT
)
CategorieOperation.objects.create(
    name = "En espèces",
    etat = Etat.objects.get(etiquette = ETAT.TERMINE),
    etiquette = CategorieOperation.ESPECES
)
CategorieOperation.objects.create(
    name = "Mobile Money",
    etat = Etat.objects.get(etiquette = ETAT.ENCOURS),
    etiquette = CategorieOperation.MOBILE_MONEY
)
CategorieOperation.objects.create(
    name = "Par chèque",
    etat = Etat.objects.get(etiquette = ETAT.ENCOURS),
    etiquette = CategorieOperation.CHEQUE
)