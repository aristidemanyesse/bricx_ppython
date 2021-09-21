from commandeApp.models import Approvisionnement
from organisationApp.models import Agence
from coreApp.models import BaseModel
from django.db import models

# Create your models here.


class Compte(BaseModel):
    name           = models.CharField(max_length = 255)
    initial_amount = models.CharField(default=0)
    etablissement  = models.IntegerField(default=0, max_length = 255, null = True, blank=True)
    numero         = models.CharField(max_length = 255, null = True, blank=True)



class TypeOperationCaisse(BaseModel):
    name           = models.CharField(max_length = 255)



class TypeMouvement(BaseModel):
    name           = models.CharField(max_length = 255)



class Reglement(BaseModel):
    reference         = models.CharField(max_length = 255, null = True, blank=True)
    mouvement = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    montant  = models.IntegerField(default=0, max_length = 255, null = True, blank=True)
    agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    mode = models.ForeignKey(ModePayement,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    commande = models.ForeignKey(Commande,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    approvisionnement = models.ForeignKey(Approvisionnement,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    etat = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    client = models.ForeignKey(Client, on_delete = models.CASCADE, related_name="agence_acces")
    utilisateur = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, related_name="utilisateur_acces")
    comment  = models.CharField(default=0, max_length = 255, null = True, blank=True)
    structure  = models.CharField(default=0, max_length = 255, null = True, blank=True)
    recouvrement = models.BooleanField(default=False)
    image = models.ImageField()


class Mouvement(BaseModel):
    name           = models.CharField(max_length = 255)
    reference         = models.CharField(max_length = 255, null = True, blank=True)
    montant  = models.IntegerField(default=0, max_length = 255, null = True, blank=True)
    type = models.ForeignKey(TypeMouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    mode = models.ForeignKey(ModePayement,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    etat = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    compte = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    comment  = models.CharField(default=0, max_length = 255, null = True, blank=True)
    structure  = models.CharField(default=0, max_length = 255, null = True, blank=True)
    numero  = models.CharField(default=0, max_length = 255, null = True, blank=True)



class Operation(BaseModel):
    reference         = models.CharField(max_length = 255, null = True, blank=True)
    montant  = models.IntegerField(default=0, max_length = 255, null = True, blank=True)
    category = models.ForeignKey(CategoryOperation,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    mouvement = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    mode = models.ForeignKey(ModePayement,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    structure  = models.CharField(default=0, max_length = 255, null = True, blank=True)
    etat = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    utilisateur = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, related_name="utilisateur_acces")
    comment  = models.CharField(default=0, max_length = 255, null = True, blank=True)
    date_approbation  = models.DateTimeField(null = True, blank=True)


class CategoryOperation(BaseModel):
    name           = models.CharField(max_length = 255)
    etiquette         = models.CharField(max_length = 255, null = True, blank=True)
    type = models.ForeignKey(TypeOperationCaisse,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    color  = models.IntegerField(default=0, max_length = 255, null = True, blank=True)


class ModePayement(BaseModel):
    name           = models.CharField(max_length = 255)
    etiquette           = models.CharField(max_length = 255)
    etat = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")




class PayementTricycle(BaseModel):
    reference         = models.CharField(max_length = 255, null = True, blank=True)
    montant  = models.IntegerField(default=0, max_length = 255, null = True, blank=True)
    mouvement = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    mode = models.ForeignKey(ModePayement,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    etat = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    tricycle = models.ForeignKey(tricycle, on_delete = models.CASCADE, related_name="agence_acces")
    utilisateur = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, related_name="utilisateur_acces")
    comment  = models.CharField(default=0, max_length = 255, null = True, blank=True)
    structure  = models.CharField(default=0, max_length = 255, null = True, blank=True)
