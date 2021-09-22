from approvisionnementApp.models import AchatStock, Approvisionnement
from commandeApp.models import Client, Commande, Tricycle
from coreApp.models import BaseModel, Etat
from django.db import models

# Create your models here.

class TypeOperationCaisse(BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)


class TypeMouvement(BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)


class TypeReglement(BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)


class CategoryOperation(BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)
    type      = models.ForeignKey(TypeOperationCaisse, on_delete = models.CASCADE, related_name="type_categorie")
    color     = models.CharField(default="", max_length = 255)


class ModePayement(BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255)
    etat      = models.ForeignKey(Etat, on_delete = models.CASCADE)


class Compte(BaseModel):
    name           = models.CharField(max_length = 255)
    initial_amount = models.IntegerField(default=0)
    etablissement  = models.CharField(max_length = 255, null = True, blank=True)
    numero         = models.CharField(max_length = 255, null = True, blank=True)



class Mouvement(BaseModel):
    name      = models.CharField(max_length = 255)
    type      = models.ForeignKey(TypeMouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="type_mouvement")
    reference = models.CharField(max_length = 255, null = True, blank=True)
    montant   = models.IntegerField(default=0, max_length = 255, null = True, blank=True)
    compte    = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_mouvement")
    employe   = models.ForeignKey("Employe", on_delete = models.CASCADE, related_name="employe_payetricycle")
    etat      = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    mode      = models.ForeignKey(ModePayement,  null = True, blank=True, on_delete = models.CASCADE, related_name="modepayement_mouvement")
    structure = models.CharField(default=0, max_length = 255, null = True, blank=True)
    numero    = models.CharField(default=0, max_length = 255, null = True, blank=True)
    comment   = models.TextField(default="")




class Reglement(BaseModel):
    reference    = models.CharField(max_length = 255, null = True, blank=True)
    mouvement    = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="mouvement_reglement")
    type         = models.ForeignKey(TypeReglement,  null = True, blank=True, on_delete = models.CASCADE, related_name="commande_reglement")
    etat         = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    client       = models.ForeignKey(Client, on_delete = models.CASCADE, related_name="client_reglement")
    recouvrement = models.BooleanField(default=False)
    image        = models.ImageField()



class ReglementApprovisionnement(BaseModel):
    reglement         = models.ForeignKey(Reglement, on_delete = models.CASCADE, related_name="reglement_approvisionnement")
    approvisionnement = models.ForeignKey(Approvisionnement, on_delete = models.CASCADE, related_name="approvisionnement_reglement")

class ReglementCommande(BaseModel):
    reglement         = models.ForeignKey(Reglement, on_delete = models.CASCADE, related_name="reglement_commande")
    commande = models.ForeignKey(Commande, on_delete = models.CASCADE, related_name="commande_reglement")


class ReglementAchatStock(BaseModel):
    reglement         = models.ForeignKey(Reglement, on_delete = models.CASCADE, related_name="reglement_achatstock")
    achatstock = models.ForeignKey(AchatStock, on_delete = models.CASCADE, related_name="achatstock_reglement")

class Operation(BaseModel):
    reference        = models.CharField(max_length = 255, null = True, blank=True)
    category         = models.ForeignKey(CategoryOperation,  null = True, blank=True, on_delete = models.CASCADE, related_name="category_operation")
    mouvement        = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="mouvement_operation")
    etat             = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    date_approbation = models.DateTimeField(null = True, blank=True)



class PayementTricycle(BaseModel):
    reference   = models.CharField(max_length = 255)
    mouvement   = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="mouvement_payetricycle")
    etat        = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    tricycle    = models.ForeignKey(Tricycle, on_delete = models.CASCADE, related_name="tricycle_paye")




class Transfertfond(BaseModel):
    reference          = models.CharField(max_length = 255)
    montant            = models.IntegerField(default=0, max_length = 255, null = True, blank=True)
    compte_source      = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_source_transfert")
    compte_destination = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_destination_transfert")
    comment            = models.TextField(default="")
    etat               = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    employe        = models.ForeignKey("Employe", on_delete = models.CASCADE, related_name="employe_transfertfond")
