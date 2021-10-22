
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from coreApp.models import BaseModel


# Create your models here.

class TypePerte(BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255)


class Brique(BaseModel):
    name      = models.CharField(max_length = 255)
    active = models.BooleanField(default=True)
    comment   = models.TextField(default="", null = True, blank=True)
    alert_stock         = models.IntegerField(default=10)
    image     = models.ImageField(max_length = 255, upload_to = "storage/images/briques/", default="", null = True, blank=True)


class Ressource(BaseModel):
    name      = models.CharField(max_length = 255)
    active = models.BooleanField(default=True)
    alert_stock         = models.IntegerField(default=10)
    comment   = models.TextField(default="", null = True, blank=True)
    image     = models.ImageField(max_length = 255, upload_to = "storage/images/ressources/", default="", null = True, blank=True)


class Production(BaseModel):
    reference             = models.CharField(max_length = 255)
    agence                = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_production")
    employe           = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_production")
    employe_rangement = models.ForeignKey("organisationApp.Employe",  null = True, blank=True, on_delete = models.CASCADE, related_name="employe_rangement_production")
    date                  = models.DateField(null = True, blank=True,)
    date_rangement        = models.DateTimeField(null = True, blank=True)
    etat                  = models.ForeignKey("coreApp.Etat", on_delete = models.CASCADE)
    montant_production    = models.IntegerField(default=0)
    montant_rangement     = models.IntegerField(default=0)
    montant_livraison     = models.IntegerField(default=0)
    comment               = models.TextField(default="", null = True, blank=True)


class LigneProduction(BaseModel):
    production = models.ForeignKey(Production, on_delete = models.CASCADE, related_name="production_ligne")
    brique     = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_ligneproduction")
    perte      = models.IntegerField(default=0)
    quantite   = models.IntegerField(default=0)


class ConsommationJour(BaseModel):
    date        = models.DateField(default="", null = True, blank=True)
    comment     = models.TextField(default="", null = True, blank=True)
    employe = models.ForeignKey("organisationApp.Employe",  null = True, blank=True, on_delete = models.CASCADE, related_name="employe_consommationjour")


class LigneConsommation(BaseModel):
    production = models.ForeignKey(Production, on_delete = models.CASCADE, related_name="production_ligneconsommation")
    ressource  = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_ligneconsommation")
    quantite   = models.IntegerField(default = 0)



class ExigenceProduction(BaseModel):
    brique   = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_exigenceproduction")
    quantite = models.IntegerField(default=0)


class LigneExigenceProduction(BaseModel):
    exigence  = models.ForeignKey(ExigenceProduction, on_delete = models.CASCADE, related_name="exigence_ligne")
    ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_exigenceligne")
    quantite  = models.IntegerField(default = 0)



class InitialBriqueAgence(BaseModel):
    agence   = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_initialbrique")
    brique   = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_initialagence")
    quantite = models.IntegerField(default=0)


class InitialRessourceAgence(BaseModel):
    agence    = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_initialressource")
    ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_initialagence")
    quantite  = models.IntegerField(default=0)



class PerteRessource(BaseModel):
    type        = models.ForeignKey(TypePerte, on_delete = models.CASCADE, related_name="type_perteressource")
    agence      = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_perteressource")
    ressource   = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_perte")
    employe = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_perteressource")
    etat        = models.ForeignKey("coreApp.Etat", on_delete = models.CASCADE)
    quantite    = models.IntegerField(default=0)
    comment     = models.IntegerField(default=0)


class PerteBrique(BaseModel):
    type        = models.ForeignKey(TypePerte, on_delete = models.CASCADE, related_name="type_pertebrique")
    agence      = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_perte")
    brique      = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_perte")
    employe = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_pertebrique")
    etat        = models.ForeignKey("coreApp.Etat", on_delete = models.CASCADE)
    quantite    = models.IntegerField(default=0)
    comment     = models.IntegerField(default=0)


class LignePerteBrique(BaseModel):
    perte    = models.ForeignKey(PerteBrique, on_delete = models.CASCADE, related_name="perte_ligne")
    brique   = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_perteligne")
    quantite = models.IntegerField(default=0)



class PayeBrique(BaseModel):
    brique          = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_paye")
    price           = models.IntegerField(default=0)
    price_rangement = models.IntegerField(default=0)
    price_livraison = models.IntegerField(default=0)


class PayeBriqueFerie(BaseModel):
    brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_payeferie")
    price = models.IntegerField(default=0)
    price_rangement = models.IntegerField(default=0)
    price_livraison = models.IntegerField(default=0)




######################################################################################################
##### SIGNAUX



