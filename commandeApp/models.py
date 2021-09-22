from productionApp.models import Brique, Ressource
from organisationApp.models import Agence, Employe
from coreApp.models import BaseModel, Etat
from django.db import models

# Create your models here.


class TypeClient(BaseModel):
    name           = models.CharField(max_length = 255)



class Client(BaseModel):
    fullname        = models.CharField(max_length = 255)
    adresse         = models.CharField(max_length = 255, null = True, blank=True)
    email            = models.EmailField(max_length = 255, null = True, blank=True)
    contact         = models.CharField(max_length = 255, null = True, blank=True)
    agence          = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="client_agence")
    type            = models.ForeignKey(TypeClient, on_delete = models.CASCADE, related_name="type_client")
    acompte_initial = models.IntegerField(default=0)
    dette_initial   = models.IntegerField(default=0)
    seuil_credit    = models.IntegerField(default=0)


class Chauffeur(BaseModel):
    fullname = models.CharField(max_length = 255)
    adresse  = models.CharField(max_length = 255, null = True, blank=True)
    contact  = models.CharField(max_length = 255, null = True, blank=True)
    etat     = models.ForeignKey(Etat, on_delete = models.CASCADE) 

class Vehicule(BaseModel):
    immatriculation = models.CharField(max_length = 255)
    modele          = models.CharField(max_length = 255, null = True, blank=True)
    marque          = models.CharField(max_length = 255, null = True, blank=True)
    etat            = models.ForeignKey(Etat,  on_delete = models.CASCADE) 



class ZoneLivraison(BaseModel):
    name   = models.CharField(max_length = 255)
    agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_zone")



class GroupeCommande(BaseModel):
    client = models.ForeignKey(Client, on_delete = models.CASCADE, related_name="client_groupecommande")
    agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_groupecommande")
    etat   = models.ForeignKey(Etat, on_delete = models.CASCADE)


class Commande(BaseModel):
    reference          = models.CharField(max_length = 255)
    groupecommande     = models.ForeignKey(GroupeCommande, on_delete = models.CASCADE, related_name="commande_groupecommande")
    agence             = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_commande")
    zonelivraison      = models.ForeignKey(ZoneLivraison, on_delete = models.CASCADE, related_name="zone_commande")
    lieu               = models.CharField(max_length = 255)
    montant            = models.IntegerField(default = 0)
    avance             = models.IntegerField(default = 0)
    taux_tva           = models.IntegerField(default = 0)
    tva                = models.IntegerField(default = 0)
    employe            = models.ForeignKey(Employe, on_delete = models.CASCADE, related_name="employe_commande")
    etat               = models.ForeignKey(Etat, on_delete = models.CASCADE) 
    comment            = models.TextField(default="");

    datelivraison      = models.DateTimeField(null = True, blank=True,)
    acompteFournisseur = models.IntegerField(default = 0)
    detteFournisseur   = models.IntegerField(default = 0)


class LigneCommande(BaseModel):
    commande = models.ForeignKey(Commande, on_delete = models.CASCADE, related_name="commande_ligne")
    brique   = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_lignecommande")
    quantite = models.IntegerField(default = 0)
    price    = models.IntegerField(default = 0)



class Livraison(BaseModel):
    reference              = models.CharField(max_length = 255)
    groupecommande         = models.ForeignKey(GroupeCommande, on_delete = models.CASCADE, related_name="groupecommande_livraison")
    agence                 = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_livraison")
    zonelivraison          = models.ForeignKey(ZoneLivraison, on_delete = models.CASCADE, related_name="zone_livraison")
    lieu                   = models.CharField(max_length = 255)
    employe                = models.ForeignKey(Employe, on_delete = models.CASCADE, related_name="employe_livraison")
    chauffeur              = models.ForeignKey(Chauffeur, on_delete = models.CASCADE, related_name="chauffeur_livraison")
    vehicule               = models.ForeignKey(Vehicule, on_delete = models.CASCADE, related_name="vehicule_livraison")
    etat                   = models.ForeignKey(Etat,  on_delete = models.CASCADE) 
    comment                = models.TextField(default="");
    datelivraison          = models.DateTimeField(null = True, blank=True)

    nom_receptionniste     = models.CharField(max_length = 255, default="")
    contact_receptionniste = models.CharField(max_length = 255, default="")
    chargement             = models.BooleanField(default=True)
    dechargement           = models.BooleanField(default=True)


class LigneLivraison(BaseModel):
    livraison = models.ForeignKey(Livraison, on_delete = models.CASCADE, related_name="livraison_ligne")
    brique    = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_lignelivraison")
    quantite  = models.IntegerField(default = 0)
    price     = models.IntegerField(default = 0)


class PrixZoneLivraison(BaseModel):
    zone   = models.ForeignKey(ZoneLivraison, on_delete = models.CASCADE, related_name="zone_prix") 
    brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_zoneprix") 
    price  = models.CharField(max_length = 255)



class Tricycle(BaseModel):
    livraison = models.ForeignKey(Livraison, on_delete = models.CASCADE, related_name="livraison_tricycle")
    montant   = models.IntegerField(default = 0)
    fullname  = models.CharField(max_length = 255)
    adresse   = models.CharField(max_length = 255, null = True, blank=True)
    contact   = models.CharField(max_length = 255, null = True, blank=True)
    etat      = models.ForeignKey(Etat,  on_delete = models.CASCADE) 
