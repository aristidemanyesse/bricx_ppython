from authApp.models import Utilisateur
from organisationApp.models import Agence
from coreApp.models import BaseModel, Etat
from django.db import models

# Create your models here.


class TypeClient(BaseModel):
    name           = models.CharField(max_length = 255)


class Client(BaseModel):
    fullname           = models.CharField(max_length = 255)
    adresse         = models.CharField(max_length = 255, null = True, blank=True)
    email         = models.CharField(max_length = 255, null = True, blank=True)
    contact  = models.CharField(max_length = 255, null = True, blank=True)
	agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
	type = models.ForeignKey(TypeClient, on_delete = models.CASCADE, related_name="agence_acces")
    acompte_initial = models.IntegerField(default=0)
    dette_initial =  models.IntegerField(default=0)
    seuil_credit =  models.IntegerField(default=0)


class GroupeCommande(BaseModel):
	client = models.ForeignKey(Client, on_delete = models.CASCADE, related_name="agence_acces")
	agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
	etat = models.ForeignKey(Etat, on_delete = models.CASCADE, related_name="agence_acces")


class Commande(BaseModel):
    reference = models.CharField(max_length = 255)
    groupecommande = models.ForeignKey(GroupeCommande,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
	agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
	zonelivraison = models.ForeignKey(ZoneLivraison, on_delete = models.CASCADE, related_name="agence_acces")
	lieu = models.CharField(max_length = 255)
    montant = models.IntegerField(default = 0)
	avance = models.IntegerField(default = 0)
    tva = models.ForeignKey(TVA, on_delete = models.CASCADE, related_name="agence_acces")
    utilisateur = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, related_name="utilisateur_acces")
	etat  = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces") 
	comment = models.TextField(default="");
	datelivraison = models.DateTimeField(null = True, blank=True,);

	acompteFournisseur = models.CharField(max_length = 255)
	detteFournisseur = models.CharField(max_length = 255)


class LigneCommande(BaseModel):
    commande = models.ForeignKey(Commande, on_delete = models.CASCADE, related_name="agence_acces")
	brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="agence_acces")
	quantite = models.IntegerField(default = 0)
	price = models.IntegerField(default = 0)



class Livraison(BaseModel):
    reference = models.CharField(max_length = 255)
    groupecommande = models.ForeignKey(GroupeCommande,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
	agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
	zonelivraison = models.ForeignKey(ZoneLivraison, on_delete = models.CASCADE, related_name="agence_acces")
	lieu = models.CharField(max_length = 255)
    utilisateur = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, related_name="utilisateur_acces")
    chauffeur = models.ForeignKey(Chauffeur, on_delete = models.CASCADE, related_name="utilisateur_acces")
    vehicule = models.ForeignKey(Vehicule, on_delete = models.CASCADE, related_name="utilisateur_acces")
	etat  = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces") 
	comment = models.TextField(default="");
	datelivraison = models.DateTimeField(null = True, blank=True,);

    nom_receptionniste = models.CharField(max_length = 255)
	contact_receptionniste = models.CharField(max_length = 255)
	chargement = models.BooleanField(default=True)
	dechargement = models.BooleanField(default=True)


class LigneLivraison(BaseModel):
    commande = models.ForeignKey(Commande, on_delete = models.CASCADE, related_name="agence_acces")
	brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="agence_acces")
	quantite = models.IntegerField(default = 0)
	price = models.IntegerField(default = 0)



class LigneAchatStock(BaseModel):
    achatstock = models.ForeignKey(AchatStock, on_delete = models.CASCADE, related_name="agence_acces")
	brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="agence_acces")
	quantite = models.IntegerField(default = 0)
	quantite_recu = models.IntegerField(default = 0)
	price = models.IntegerField(default = 0)



class Fournisseur(BaseModel):
    fullname           = models.CharField(max_length = 255)
	agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    adresse         = models.CharField(max_length = 255, null = True, blank=True)
    email         = models.CharField(max_length = 255, null = True, blank=True)
    contact  = models.CharField(max_length = 255, null = True, blank=True)
	description = models.TextField(default="")
    acompte_initial = models.IntegerField(default=0)
    dette_initial =  models.IntegerField(default=0)
    seuil_credit =  models.IntegerField(default=0)



class Approvisionnement(BaseModel):
    reference = models.CharField(default = 0)
	montant = models.IntegerField(default = 0)
	avance = models.IntegerField(default = 0)
	reste = models.CharField(max_length = 255)
	transport = models.CharField(max_length = 255);
	reglement = models.ForeignKey(Reglement,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
	fournisseur = models.ForeignKey(Fournisseur,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces");
	agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    utilisateur = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, related_name="utilisateur_acces")
    utilisateur_reception = models.ForeignKey(Utilisateur,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
	etat  = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces") 
	comment = models.TextField(default="");
	datelivraison = models.DateTimeField(null = True, blank=True,);

	acompteFournisseur = models.CharField(max_length = 255)
	detteFournisseur = models.CharField(max_length = 255)


class LigneApprovisionnement(BaseModel):
    approvisionnement = models.ForeignKey(Approvisionnement, on_delete = models.CASCADE, related_name="agence_acces")
	ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="agence_acces")
	quantite = models.IntegerField(default = 0)
	quantite_recu = models.IntegerField(default = 0)
	price = models.IntegerField(default = 0)




class Chauffeur(BaseModel):
    fullname           = models.CharField(max_length = 255)
    adresse         = models.CharField(max_length = 255, null = True, blank=True)
    contact  = models.CharField(max_length = 255, null = True, blank=True)
	etat  = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces") 



class Vehicule(BaseModel):
    immatriculation           = models.CharField(max_length = 255)
    modele         = models.CharField(max_length = 255, null = True, blank=True)
    marque  = models.CharField(max_length = 255, null = True, blank=True)
	etat  = models.ForeignKey(Etat,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces") 



class ZoneLivraison(BaseModel):
    name    = models.CharField(max_length = 255)


class PrixZoneLivraison(BaseModel):
	zone  = models.ForeignKey(ZoneLivraison,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces") 
	brique  = models.ForeignKey(Brique,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces") 
	price = models.CharField(max_length = 255)
