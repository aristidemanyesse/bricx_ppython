
from django.db import models

import productionApp.models as production_models
import organisationApp.models as organisation_models
import clientApp.models as client_models
import coreApp.models as core_models
import comptabilityApp.models as comptability_models
# Create your models here.


class Fournisseur(core_models.BaseModel):
    fullname        = models.CharField(max_length = 255)
    agence          = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_fournisseur")
    adresse         = models.CharField(max_length = 255, null = True, blank=True)
    email           = models.CharField(max_length = 255, null = True, blank=True)
    contact         = models.CharField(max_length = 255, null = True, blank=True)
    description     = models.TextField(default="")
    acompte_initial = models.IntegerField(default=0)
    dette_initial   = models.IntegerField(default=0)
    seuil_credit    = models.IntegerField(default=0)


class AchatStock(core_models.BaseModel):
    reference         = models.CharField(max_length = 255)
    agence            = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_achatstock")
    montant           = models.IntegerField(default = 0)
    avance            = models.IntegerField(default = 0)    
    reste             = models.IntegerField(default = 0)    
    fournisseur       = models.ForeignKey(Fournisseur, on_delete = models.CASCADE, related_name="fournisseur_achatstock")
    etat              = models.ForeignKey(core_models.Etat,  on_delete = models.CASCADE) 
    employe           = models.ForeignKey(organisation_models.Employe, on_delete = models.CASCADE, related_name="employe_achatstock")
    employe_reception = models.ForeignKey(organisation_models.Employe, on_delete = models.CASCADE, related_name="employe_reception_achatstock")
    comment           = models.TextField(default="");
    datelivraison     = models.DateTimeField(null = True, blank=True)


class LigneAchatStock(core_models.BaseModel):
    achatstock    = models.ForeignKey(AchatStock, on_delete = models.CASCADE, related_name="achatstock_ligne")
    brique        = models.ForeignKey(production_models.Brique, on_delete = models.CASCADE, related_name="brique_ligneachatstock")
    quantite      = models.IntegerField(default = 0)
    quantite_recu = models.IntegerField(default = 0)
    price         = models.IntegerField(default = 0)




class Approvisionnement(core_models.BaseModel):
    reference          = models.CharField(max_length = 255)
    montant            = models.IntegerField(default = 0)
    avance             = models.IntegerField(default = 0)
    reste              = models.IntegerField(default = 0)
    transport          = models.IntegerField(default = 0)
    fournisseur        = models.ForeignKey(Fournisseur, on_delete = models.CASCADE, related_name="fournisseur_approvisionnement");
    agence             = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_approvisionnement")
    employe            = models.ForeignKey(organisation_models.Employe, on_delete = models.CASCADE, related_name="employe_approvisionnement")
    employe_reception  = models.ForeignKey(organisation_models.Employe,  null = True, blank=True, on_delete = models.CASCADE, related_name="employe_reception_approvisionnement")
    etat               = models.ForeignKey(core_models.Etat, on_delete = models.CASCADE) 
    comment            = models.TextField(default="");
    datelivraison      = models.DateTimeField(null = True, blank=True,);

    acompteFournisseur = models.IntegerField(default = 0)
    detteFournisseur   = models.IntegerField(default = 0)


class LigneApprovisionnement(core_models.BaseModel):
    approvisionnement = models.ForeignKey(Approvisionnement, on_delete = models.CASCADE, related_name="approvisionnement_ligne")
    ressource         = models.ForeignKey(production_models.Ressource, on_delete = models.CASCADE, related_name="ressource_ligneapprovisionnement")
    quantite          = models.IntegerField(default = 0)
    quantite_recu     = models.IntegerField(default = 0)
    price             = models.IntegerField(default = 0)
