from organisationApp.models import Employe
from commandeApp.models import Approvisionnement, Client, Commande, Tricycle
from coreApp.models import BaseModel, Etat
from django.db import models

# Create your models here.

class TypeOperationCaisse(BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)


class TypeMouvement(BaseModel):
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
    reference = models.CharField(max_length = 255, null = True, blank=True)
    montant   = models.IntegerField(default=0, max_length = 255, null = True, blank=True)
    type      = models.ForeignKey(TypeMouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="type_mouvement")
    etat      = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    compte    = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_mouvement")
    comment   = models.CharField(default=0, max_length = 255, null = True, blank=True)
    mode      = models.ForeignKey(ModePayement,  null = True, blank=True, on_delete = models.CASCADE, related_name="modepayement_mouvement")
    structure = models.CharField(default=0, max_length = 255, null = True, blank=True)
    numero    = models.CharField(default=0, max_length = 255, null = True, blank=True)




class Reglement(BaseModel):
    reference         = models.CharField(max_length = 255, null = True, blank=True)
    mouvement         = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="mouvement_reglement")
    commande          = models.ForeignKey(Commande,  null = True, blank=True, on_delete = models.CASCADE, related_name="commande_reglement")
    approvisionnement = models.ForeignKey(Approvisionnement,  null = True, blank=True, on_delete = models.CASCADE, related_name="approvisionnement_reglement")
    etat              = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    client            = models.ForeignKey(Client, on_delete = models.CASCADE, related_name="client_reglement")
    employe       = models.ForeignKey(Employe, on_delete = models.CASCADE, related_name="employe_reglement")
    comment           = models.CharField(default=0, max_length = 255, null = True, blank=True)
    recouvrement      = models.BooleanField(default=False)
    image             = models.ImageField()



class Operation(BaseModel):
    reference        = models.CharField(max_length = 255, null = True, blank=True)
    category         = models.ForeignKey(CategoryOperation,  null = True, blank=True, on_delete = models.CASCADE, related_name="category_operation")
    mouvement        = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="mouvement_operation")
    etat             = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    employe      = models.ForeignKey(Employe, on_delete = models.CASCADE, related_name="employe_operation")
    comment          = models.TextField(default="")
    date_approbation = models.DateTimeField(null = True, blank=True)



class PayementTricycle(BaseModel):
    reference   = models.CharField(max_length = 255)
    mouvement   = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="mouvement_payetricycle")
    etat        = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    tricycle    = models.ForeignKey(Tricycle, on_delete = models.CASCADE, related_name="tricycle_paye")
    employe = models.ForeignKey(Employe, on_delete = models.CASCADE, related_name="employe_payetricycle")
    comment     = models.TextField(default="")



class Transfertfond(BaseModel):
    reference          = models.CharField(max_length = 255)
    montant            = models.IntegerField(default=0, max_length = 255, null = True, blank=True)
    compte_source      = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_source_transfert")
    compte_destination = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_destination_transfert")
    comment            = models.TextField(default="")
    etat               = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    employe        = models.ForeignKey(Employe, on_delete = models.CASCADE, related_name="employe_transfertfond")
