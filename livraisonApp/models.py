
from django.db import models

from coreApp.models import BaseModel

# Create your models here.



class Chauffeur(BaseModel):
    name = models.CharField(max_length = 255)
    adresse  = models.CharField(max_length = 255, null = True, blank=True)
    contact  = models.CharField(max_length = 255, null = True, blank=True)
    etat     = models.ForeignKey("coreApp.Etat", on_delete = models.CASCADE) 



class Vehicule(BaseModel):
    immatriculation = models.CharField(max_length = 255)
    modele          = models.CharField(max_length = 255, null = True, blank=True)
    marque          = models.CharField(max_length = 255, null = True, blank=True)
    etat            = models.ForeignKey("coreApp.Etat",  on_delete = models.CASCADE) 



class Livraison(BaseModel):
    reference              = models.CharField(max_length = 255)
    groupecommande         = models.ForeignKey("commandeApp.GroupeCommande", on_delete = models.CASCADE, related_name="groupecommande_livraison")
    agence                 = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_livraison")
    lieu                   = models.CharField(max_length = 255)
    employe                = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_livraison")
    chauffeur              = models.ForeignKey(Chauffeur, on_delete = models.CASCADE, related_name="chauffeur_livraison")
    vehicule               = models.ForeignKey(Vehicule, on_delete = models.CASCADE, related_name="vehicule_livraison")
    etat                   = models.ForeignKey("coreApp.Etat",  on_delete = models.CASCADE) 
    comment                = models.TextField(default="");
    datelivraison          = models.DateTimeField(null = True, blank=True)

    nom_receptionniste     = models.CharField(max_length = 255, default="")
    contact_receptionniste = models.CharField(max_length = 255, default="")
    chargement             = models.BooleanField(default=True)
    dechargement           = models.BooleanField(default=True)



class LigneLivraison(BaseModel):
    livraison = models.ForeignKey(Livraison, on_delete = models.CASCADE, related_name="livraison_ligne")
    brique    = models.ForeignKey("productionApp.Brique", on_delete = models.CASCADE, related_name="brique_lignelivraison")
    quantite  = models.IntegerField(default = 0)
    price     = models.IntegerField(default = 0)




class Tricycle(BaseModel):
    livraison = models.ForeignKey(Livraison, on_delete = models.CASCADE, related_name="livraison_tricycle")
    montant   = models.IntegerField(default = 0)
    fullname  = models.CharField(max_length = 255)
    adresse   = models.CharField(max_length = 255, null = True, blank=True)
    contact   = models.CharField(max_length = 255, null = True, blank=True)
    etat      = models.ForeignKey("coreApp.Etat",  on_delete = models.CASCADE) 
