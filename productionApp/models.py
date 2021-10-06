import approvisionnementApp.models as appro_models
import commandeApp.models as commande_models
import livraisonApp.models as livraison_models
import productionApp.models as production_models
import organisationApp.models as organisation_models
import clientApp.models as client_models
import coreApp.models as core_models
import comptabilityApp.models as comptability_models
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


# Create your models here.

class TypePerte(core_models.BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255)


class Brique(core_models.BaseModel):
    name      = models.CharField(max_length = 255)
    active = models.BooleanField(default=True)
    comment   = models.TextField(default="", null = True, blank=True)
    image     = models.ImageField(max_length = 255, upload_to = "storage/images/briques/", default="", null = True, blank=True)


class Ressource(core_models.BaseModel):
    name      = models.CharField(max_length = 255)
    active = models.BooleanField(default=True)
    comment   = models.TextField(default="", null = True, blank=True)
    image     = models.ImageField(max_length = 255, upload_to = "storage/images/ressources/", default="", null = True, blank=True)


class Production(core_models.BaseModel):
    reference             = models.CharField(max_length = 255)
    agence                = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_production")
    employe           = models.ForeignKey(organisation_models.Employe, on_delete = models.CASCADE, related_name="employe_production")
    employe_rangement = models.ForeignKey(organisation_models.Employe,  null = True, blank=True, on_delete = models.CASCADE, related_name="employe_rangement_production")
    date                  = models.DateField(null = True, blank=True,)
    date_rangement        = models.DateTimeField(null = True, blank=True)
    etat                  = models.ForeignKey(core_models.Etat, on_delete = models.CASCADE)
    montant_production    = models.IntegerField(default=0)
    montant_rangement     = models.IntegerField(default=0)
    montant_livraison     = models.IntegerField(default=0)
    comment               = models.TextField(default="", null = True, blank=True)


class LigneProduction(core_models.BaseModel):
    production = models.ForeignKey(Production, on_delete = models.CASCADE, related_name="production_ligne")
    brique     = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_ligneproduction")
    perte      = models.IntegerField(default=0)
    quantite   = models.IntegerField(default=0)


class ConsommationJour(core_models.BaseModel):
    date        = models.DateField(default="", null = True, blank=True)
    comment     = models.TextField(default="", null = True, blank=True)
    employe = models.ForeignKey(organisation_models.Employe,  null = True, blank=True, on_delete = models.CASCADE, related_name="employe_consommationjour")


class LigneConsommation(core_models.BaseModel):
    production = models.ForeignKey(Production, on_delete = models.CASCADE, related_name="production_ligneconsommation")
    ressource  = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_ligneconsommation")
    quantite   = models.IntegerField(default = 0)



class ExigenceProduction(core_models.BaseModel):
    brique   = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_exigenceproduction")
    quantite = models.IntegerField(default=0)


class LigneExigenceProduction(core_models.BaseModel):
    exigence  = models.ForeignKey(ExigenceProduction, on_delete = models.CASCADE, related_name="exigence_ligne")
    ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_exigenceligne")
    quantite  = models.IntegerField(default = 0)



class InitialBriqueAgence(core_models.BaseModel):
    agence   = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_initialbrique")
    brique   = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_initialagence")
    quantite = models.IntegerField(default=0)


class InitialRessourceAgence(core_models.BaseModel):
    agence    = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_initialressource")
    ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_initialagence")
    quantite  = models.IntegerField(default=0)



class PerteRessource(core_models.BaseModel):
    type        = models.ForeignKey(TypePerte, on_delete = models.CASCADE, related_name="type_perteressource")
    agence      = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_perteressource")
    ressource   = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_perte")
    employe = models.ForeignKey(organisation_models.Employe, on_delete = models.CASCADE, related_name="employe_perteressource")
    etat        = models.ForeignKey(core_models.Etat, on_delete = models.CASCADE)
    quantite    = models.IntegerField(default=0)
    comment     = models.IntegerField(default=0)


class PerteBrique(core_models.BaseModel):
    type        = models.ForeignKey(TypePerte, on_delete = models.CASCADE, related_name="type_pertebrique")
    agence      = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_perte")
    brique      = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_perte")
    employe = models.ForeignKey(organisation_models.Employe, on_delete = models.CASCADE, related_name="employe_pertebrique")
    etat        = models.ForeignKey(core_models.Etat, on_delete = models.CASCADE)
    quantite    = models.IntegerField(default=0)
    comment     = models.IntegerField(default=0)


class LignePerteBrique(core_models.BaseModel):
    perte    = models.ForeignKey(PerteBrique, on_delete = models.CASCADE, related_name="perte_ligne")
    brique   = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_perteligne")
    quantite = models.IntegerField(default=0)



class TransfertStock(core_models.BaseModel):
    reference          = models.CharField(max_length = 255)
    agence             = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_transfertstock")
    groupecommande_old = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="old_groupecommande_transfertstock")
    groupecommande_new = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="new_groupecommande_transfertstock")
    employe        = models.ForeignKey(organisation_models.Employe,  null = True, blank=True, on_delete = models.CASCADE, related_name="employe_transfertstock")


class LigneTransfertStock(core_models.BaseModel):
    transfert      = models.ForeignKey(TransfertStock, on_delete = models.CASCADE, related_name="transfert_ligne")
    brique         = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_transfertligne")
    quantite_avant = models.IntegerField(default=0)
    quantite_apres = models.IntegerField(default=0)


class PayeBrique(core_models.BaseModel):
    brique          = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_paye")
    price           = models.IntegerField(default=0)
    price_rangement = models.IntegerField(default=0)
    price_livraison = models.IntegerField(default=0)


class PayeBriqueFerie(core_models.BaseModel):
    brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_payeferie")
    price = models.IntegerField(default=0)
    price_rangement = models.IntegerField(default=0)
    price_livraison = models.IntegerField(default=0)




######################################################################################################
##### SIGNAUX



