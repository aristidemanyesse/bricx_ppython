import approvisionnementApp.models as appro_models
import commandeApp.models as commande_models
import livraisonApp.models as livraison_models
import productionApp.models as production_models
import organisationApp.models as organisation_models
import clientApp.models as client_models
import coreApp.models as core_models
import comptabilityApp.models as comptability_models
from django.db import models

# Create your models here.



class Chauffeur(core_models.BaseModel):
    name = models.CharField(max_length = 255)
    adresse  = models.CharField(max_length = 255, null = True, blank=True)
    contact  = models.CharField(max_length = 255, null = True, blank=True)
    etat     = models.ForeignKey(core_models.Etat, on_delete = models.CASCADE) 



class Vehicule(core_models.BaseModel):
    immatriculation = models.CharField(max_length = 255)
    modele          = models.CharField(max_length = 255, null = True, blank=True)
    marque          = models.CharField(max_length = 255, null = True, blank=True)
    etat            = models.ForeignKey(core_models.Etat,  on_delete = models.CASCADE) 



class Livraison(core_models.BaseModel):
    reference              = models.CharField(max_length = 255)
    groupecommande         = models.ForeignKey(commande_models.GroupeCommande, on_delete = models.CASCADE, related_name="groupecommande_livraison")
    agence                 = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_livraison")
    lieu                   = models.CharField(max_length = 255)
    employe                = models.ForeignKey(organisation_models.Employe, on_delete = models.CASCADE, related_name="employe_livraison")
    chauffeur              = models.ForeignKey(Chauffeur, on_delete = models.CASCADE, related_name="chauffeur_livraison")
    vehicule               = models.ForeignKey(Vehicule, on_delete = models.CASCADE, related_name="vehicule_livraison")
    etat                   = models.ForeignKey(core_models.Etat,  on_delete = models.CASCADE) 
    comment                = models.TextField(default="");
    datelivraison          = models.DateTimeField(null = True, blank=True)

    nom_receptionniste     = models.CharField(max_length = 255, default="")
    contact_receptionniste = models.CharField(max_length = 255, default="")
    chargement             = models.BooleanField(default=True)
    dechargement           = models.BooleanField(default=True)



class LigneLivraison(core_models.BaseModel):
    livraison = models.ForeignKey(Livraison, on_delete = models.CASCADE, related_name="livraison_ligne")
    brique    = models.ForeignKey(production_models.Brique, on_delete = models.CASCADE, related_name="brique_lignelivraison")
    quantite  = models.IntegerField(default = 0)
    price     = models.IntegerField(default = 0)




class Tricycle(core_models.BaseModel):
    livraison = models.ForeignKey(Livraison, on_delete = models.CASCADE, related_name="livraison_tricycle")
    montant   = models.IntegerField(default = 0)
    fullname  = models.CharField(max_length = 255)
    adresse   = models.CharField(max_length = 255, null = True, blank=True)
    contact   = models.CharField(max_length = 255, null = True, blank=True)
    etat      = models.ForeignKey(core_models.Etat,  on_delete = models.CASCADE) 
