
from django.db import models

import approvisionnementApp.models as appro_models
import commandeApp.models as commande_models
import livraisonApp.models as livraison_models
import productionApp.models as production_models
import organisationApp.models as organisation_models
import clientApp.models as client_models
import coreApp.models as core_models
import comptabilityApp.models as comptability_models
# Create your models here.

class TypeOperationCaisse(core_models.BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)


class TypeMouvement(core_models.BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)


class TypeReglement(core_models.BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)


class CategoryOperation(core_models.BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)
    type      = models.ForeignKey(TypeOperationCaisse, on_delete = models.CASCADE, related_name="type_categorie")
    color     = models.CharField(default="", max_length = 255)


class ModePayement(core_models.BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255)
    etat      = models.ForeignKey(core_models.Etat, on_delete = models.CASCADE)


class Compte(core_models.BaseModel):
    name           = models.CharField(max_length = 255)
    initial_amount = models.IntegerField(default=0)
    etablissement  = models.CharField(max_length = 255, null = True, blank=True)
    numero         = models.CharField(max_length = 255, null = True, blank=True)
    agence = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_compte")



class Mouvement(core_models.BaseModel):
    name      = models.CharField(max_length = 255)
    type      = models.ForeignKey(TypeMouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="type_mouvement")
    reference = models.CharField(max_length = 255, null = True, blank=True)
    montant   = models.IntegerField(default=0)
    compte    = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_mouvement")
    employe   = models.ForeignKey(organisation_models.Employe, on_delete = models.CASCADE, related_name="employe_payetricycle")
    etat      = models.ForeignKey(core_models.Etat,  null = True, blank=True, on_delete = models.CASCADE)
    mode      = models.ForeignKey(ModePayement,  null = True, blank=True, on_delete = models.CASCADE, related_name="modepayement_mouvement")
    structure = models.CharField(default=0, max_length = 255, null = True, blank=True)
    numero    = models.CharField(default=0, max_length = 255, null = True, blank=True)
    comment   = models.TextField(default="")




class Reglement(core_models.BaseModel):
    reference    = models.CharField(max_length = 255, null = True, blank=True)
    type         = models.ForeignKey(TypeReglement,  null = True, blank=True, on_delete = models.CASCADE, related_name="commande_reglement")
    mouvement    = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="mouvement_reglement")
    etat         = models.ForeignKey(core_models.Etat,  null = True, blank=True, on_delete = models.CASCADE)
    recouvrement = models.BooleanField(default=False)
    image        = models.ImageField()



class ReglementApprovisionnement(core_models.BaseModel):
    reglement         = models.ForeignKey(Reglement, on_delete = models.CASCADE, related_name="reglement_approvisionnement")
    approvisionnement = models.ForeignKey(appro_models.Approvisionnement, on_delete = models.CASCADE, related_name="approvisionnement_reglement")

class ReglementCommande(core_models.BaseModel):
    reglement         = models.ForeignKey(Reglement, on_delete = models.CASCADE, related_name="reglement_commande")
    commande = models.ForeignKey(commande_models.Commande, on_delete = models.CASCADE, related_name="commande_reglement")


class ReglementAchatStock(core_models.BaseModel):
    reglement         = models.ForeignKey(Reglement, on_delete = models.CASCADE, related_name="reglement_achatstock")
    achatstock = models.ForeignKey(appro_models.AchatStock, on_delete = models.CASCADE, related_name="achatstock_reglement")

class ReglementTricycle(core_models.BaseModel):
    reglement         = models.ForeignKey(Reglement, on_delete = models.CASCADE, related_name="reglement_tricycle")
    tricycle = models.ForeignKey(livraison_models.Tricycle, on_delete = models.CASCADE, related_name="tricycle_reglement")


class Operation(core_models.BaseModel):
    reference        = models.CharField(max_length = 255, null = True, blank=True)
    category         = models.ForeignKey(CategoryOperation,  null = True, blank=True, on_delete = models.CASCADE, related_name="category_operation")
    mouvement        = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="mouvement_operation")
    etat             = models.ForeignKey(core_models.Etat,  null = True, blank=True, on_delete = models.CASCADE)
    date_approbation = models.DateTimeField(null = True, blank=True)


class Transfertfond(core_models.BaseModel):
    reference          = models.CharField(max_length = 255)
    montant            = models.IntegerField(default=0)
    compte_source      = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_source_transfert")
    compte_destination = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_destination_transfert")
    etat               = models.ForeignKey(core_models.Etat,  null = True, blank=True, on_delete = models.CASCADE)
    employe            = models.ForeignKey(organisation_models.Employe, on_delete = models.CASCADE, related_name="employe_transfertfond")
    comment            = models.TextField(default="")
