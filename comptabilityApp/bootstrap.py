
from comptabilityApp.models import CategoryOperation, ModePayement, TypeMouvement, TypeOperationCaisse
from coreApp.models import Etat


def run():
    TypeOperationCaisse.objects.create(
    name = "Opération de dépot",
    etiquette = TypeOperationCaisse.DEPOT,
    protected = True
    )
    TypeOperationCaisse.objects.create(
        name = "Opération de retrait",
        etiquette = TypeOperationCaisse.RETRAIT,
        protected = True
    )


    TypeMouvement.objects.create(
        name = "Mouvement de dépot",
        etiquette = TypeMouvement.DEPOT,        
        protected = True
    )
    TypeMouvement.objects.create(
        name = "Mouvement de retrait",
        etiquette = TypeMouvement.RETRAIT,
        protected = True
    )


    ModePayement.objects.create(
        name = "En espèces",
        etat = Etat.objects.get(etiquette = Etat.TERMINE),
        etiquette = ModePayement.ESPECES,
        protected = True
    )
    ModePayement.objects.create(
        name = "Crédit / Prélèvement sur acompte",
        etat = Etat.objects.get(etiquette = Etat.TERMINE),
        etiquette = ModePayement.PRELEVEMENT,
        protected = True
    )
    ModePayement.objects.create(
        name = "Mobile Money",
        etat = Etat.objects.get(etiquette = Etat.EN_COURS),
        protected = True
    )
    ModePayement.objects.create(
        name = "Par chèque",
        etat = Etat.objects.get(etiquette = Etat.EN_COURS),
        protected = True
    )
    ModePayement.objects.create(
        name = "Par virement bancaire",
        etat = Etat.objects.get(etiquette = Etat.EN_COURS),
        protected = True
    )



    CategoryOperation.objects.create(
        name = "Remboursement par le fournisseur",
        etiquette = CategoryOperation.REFUND_FOURNISSEUR,
        type = TypeOperationCaisse.objects.get(etiquette = TypeOperationCaisse.DEPOT),
    )
    CategoryOperation.objects.create(
        name = "Transfert sur le compte",
        etiquette = CategoryOperation.TRANSFERT_DEPOT,
        type = TypeOperationCaisse.objects.get(etiquette = TypeOperationCaisse.DEPOT),
    )
    CategoryOperation.objects.create(
        name = "Autre entrée",
        type = TypeOperationCaisse.objects.get(etiquette = TypeOperationCaisse.DEPOT),
    )

    CategoryOperation.objects.create(
        name = "Remboursement du client",
        type = TypeOperationCaisse.objects.get(etiquette = TypeOperationCaisse.RETRAIT),
        etiquette = CategoryOperation.REFUND_CLIENT
    )
    CategoryOperation.objects.create(
        name = "Frais de Transport",
        type = TypeOperationCaisse.objects.get(etiquette = TypeOperationCaisse.RETRAIT),
        etiquette = CategoryOperation.TRANSPORT
    )
    CategoryOperation.objects.create(
        name = "Main d'oeuvre de production",
        type = TypeOperationCaisse.objects.get(etiquette = TypeOperationCaisse.RETRAIT),
        etiquette = CategoryOperation.MAIN_D_OEUVRE
    )
    CategoryOperation.objects.create(
        name = "Payement du loyer",
        type = TypeOperationCaisse.objects.get(etiquette = TypeOperationCaisse.RETRAIT),
    )
    CategoryOperation.objects.create(
        name = "Réglement de facture CIE / SODECI",
        type = TypeOperationCaisse.objects.get(etiquette = TypeOperationCaisse.RETRAIT),
    )
    CategoryOperation.objects.create(
        name = "Réglement d'autres factures",
        type = TypeOperationCaisse.objects.get(etiquette = TypeOperationCaisse.RETRAIT),
    )
    CategoryOperation.objects.create(
        name = "Autre dépense",
        type = TypeOperationCaisse.objects.get(etiquette = TypeOperationCaisse.RETRAIT),
    )


    
    print("Initialisation du module de Comptabilité")