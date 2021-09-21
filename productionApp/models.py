from coreApp.models import Etat
from django.db import models

# Create your models here.

class TypeBrique(BaseModel):
    name = models.CharField(max_length = 255)


class Brique(BaseModel):
    name = models.IntegerField(default=0)
    is_active = models.BooleanField(default=0)
    comment = models.IntegerField(default=0)
    image = models.ImageField()


class Ressource(BaseModel):
    name = models.IntegerField(default=0)
    is_active = models.BooleanField(default=0)
    comment = models.IntegerField(default=0)
    image = models.ImageField()


class Production(BaseModel):
    reference  = models.IntegerField(default=0)
    agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    utilisateur = models.ForeignKey(Utilisateur,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    utilisateur_rangement = models.ForeignKey(Utilisateur,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    date = models.IntegerField(default=0)
    date_rangement = models.IntegerField(default=0)
    etat = models.ForeignKey(Etat, on_delete = models.CASCADE, related_name="agence_acces")
    montant_production = models.IntegerField(default=0)
    montant_rangement = models.IntegerField(default=0)
    montant_livraison = models.IntegerField(default=0)
    comment = models.IntegerField(default=0)


class LigneProduction(BaseModel):
    production = models.ForeignKey(Production, on_delete = models.CASCADE, related_name="agence_acces")
    brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="agence_acces")
    perte = models.IntegerField(default=0)
    quantite = models.IntegerField(default=0)


class ConsommationJour(BaseModel):
    date           = models.DateField(default="")
    comment         = models.TextField(max_length = 255, null = True, blank=True)
    utilisateur = models.ForeignKey(Utilisateur,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")


class LigneConsommation(BaseModel):
    production = models.ForeignKey(Production, on_delete = models.CASCADE, related_name="agence_acces")
	ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="agence_acces")
	quantite = models.IntegerField(default = 0)



class ExigenceProduction(BaseModel):
    brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="agence_acces")
    quantite = models.IntegerField(default=0)


class LigneExigenceProduction(BaseModel):
    exigence = models.ForeignKey(ExigenceProduction, on_delete = models.CASCADE, related_name="agence_acces")
	ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="agence_acces")
	quantite = models.IntegerField(default = 0)



class InitialBriqueAgence(BaseModel):
    agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="agence_acces")
    quantite = models.IntegerField(default=0)


class InitialRessourceAgence(BaseModel):
    agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="agence_acces")
    quantite = models.IntegerField(default=0)



class PerteRessource(BaseModel):
    type = models.ForeignKey(TypePerte, on_delete = models.CASCADE, related_name="agence_acces")
    agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="agence_acces")
    utilisateur = models.ForeignKey(Utilisateur,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    etat = models.ForeignKey(Etat, on_delete = models.CASCADE, related_name="agence_acces")
    quantite = models.IntegerField(default=0)
    comment = models.IntegerField(default=0)


class PerteBrique(BaseModel):
    type = models.ForeignKey(TypePerte, on_delete = models.CASCADE, related_name="agence_acces")
    agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="agence_acces")
    utilisateur = models.ForeignKey(Utilisateur,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    etat = models.ForeignKey(Etat, on_delete = models.CASCADE, related_name="agence_acces")
    quantite = models.IntegerField(default=0)
    comment = models.IntegerField(default=0)


class LignePerteBrique(BaseModel):
    perte = models.ForeignKey(PerteBrique, on_delete = models.CASCADE, related_name="agence_acces")
    brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="agence_acces")
    quantite = models.IntegerField(default=0)




class LigneTransfertStock(BaseModel):
    transfert = models.ForeignKey(TransfertStock, on_delete = models.CASCADE, related_name="agence_acces")
    brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="agence_acces")
    quantite_avant = models.IntegerField(default=0)
    quantite_apres = models.IntegerField(default=0)


class PayeBrique(BaseModel):
    brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="agence_acces")
    price = models.IntegerField(default=0)
    price_rangement = models.IntegerField(default=0)
    price_livraison = models.IntegerField(default=0)


class PayeBriqueFerie(BaseModel):
    brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="agence_acces")
    price = models.IntegerField(default=0)
    price_rangement = models.IntegerField(default=0)
    price_livraison = models.IntegerField(default=0)