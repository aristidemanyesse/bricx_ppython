from authApp.models import Utilisateur
from commandeApp.models import Approvisionnement, Client, Commande
from organisationApp.models import Agence
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
    mode      = models.ForeignKey(ModePayement,  null = True, blank=True, on_delete = models.CASCADE, related_name="modepayement_mouvement")
    etat      = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    compte    = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_mouvement")
    comment   = models.CharField(default=0, max_length = 255, null = True, blank=True)
    structure = models.CharField(default=0, max_length = 255, null = True, blank=True)
    numero    = models.CharField(default=0, max_length = 255, null = True, blank=True)




class Reglement(BaseModel):
    reference         = models.CharField(max_length = 255, null = True, blank=True)
    mouvement         = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="mouvement_reglement")
    montant           = models.IntegerField(default=0, max_length = 255, null = True, blank=True)
    agence            = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_reference")
    mode              = models.ForeignKey(ModePayement,  null = True, blank=True, on_delete = models.CASCADE, related_name="modepaye_reglement")
    commande          = models.ForeignKey(Commande,  null = True, blank=True, on_delete = models.CASCADE, related_name="commande_reglement")
    approvisionnement = models.ForeignKey(Approvisionnement,  null = True, blank=True, on_delete = models.CASCADE, related_name="approvisionnement_reglement")
    etat              = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    client            = models.ForeignKey(Client, on_delete = models.CASCADE, related_name="client_reglement")
    utilisateur       = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, related_name="utilisateur_reglement")
    comment           = models.CharField(default=0, max_length = 255, null = True, blank=True)
    structure         = models.CharField(default=0, max_length = 255, null = True, blank=True)
    recouvrement      = models.BooleanField(default=False)
    image             = models.ImageField()



class Operation(BaseModel):
    reference        = models.CharField(max_length = 255, null = True, blank=True)
    montant          = models.IntegerField(default=0)
    category         = models.ForeignKey(CategoryOperation,  null = True, blank=True, on_delete = models.CASCADE, related_name="category_operation")
    mouvement        = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="mouvement_operation")
    mode             = models.ForeignKey(ModePayement,  null = True, blank=True, on_delete = models.CASCADE, related_name="modepaye_operation")
    structure        = models.CharField(default="", max_length = 255)
    etat             = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    agence           = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_operation")
    utilisateur      = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, related_name="utilisateur_operation")
    comment          = models.TextField(default="")
    date_approbation = models.DateTimeField(null = True, blank=True)



class PayementTricycle(BaseModel):
    reference   = models.CharField(max_length = 255)
    montant     = models.IntegerField(default=0, max_length = 255, null = True, blank=True)
    mouvement   = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="mouvement_payetricycle")
    mode        = models.ForeignKey(ModePayement,  null = True, blank=True, on_delete = models.CASCADE, related_name="modepaye_payetricycle")
    etat        = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE)
    agence      = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_payetricycle")
    tricycle    = models.ForeignKey(Tricycle, on_delete = models.CASCADE, related_name="tricycle_paye")
    utilisateur = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, related_name="utilisateur_payetricycle")
    comment     = models.TextField(default="")
    structure   = models.CharField(default="", max_length = 255)
