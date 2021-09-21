from authApp.models import Utilisateur
from organisationApp.models import Agence
from coreApp.models import BaseModel, Etat
from django.db import models

# Create your models here.

class TypePerte(BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255)


class Brique(BaseModel):
    name      = models.CharField(max_length = 255)
    is_active = models.BooleanField(default=True)
    comment   = models.TextField(default="")
    image     = models.ImageField()


class Ressource(BaseModel):
    name      = models.CharField(max_length = 255)
    is_active = models.BooleanField(default=True)
    comment   = models.TextField(default="")
    image     = models.ImageField()


class Production(BaseModel):
    reference             = models.CharField(max_length = 255)
    agence                = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_production")
    utilisateur           = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, related_name="utilisateur_production")
    utilisateur_rangement = models.ForeignKey(Utilisateur,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_rangement_production")
    date                  = models.DateField(null = True, blank=True,)
    date_rangement        = models.DateTimeField(null = True, blank=True)
    etat                  = models.ForeignKey(Etat, on_delete = models.CASCADE)
    montant_production    = models.IntegerField(default=0)
    montant_rangement     = models.IntegerField(default=0)
    montant_livraison     = models.IntegerField(default=0)
    comment               = models.TextField(default="")


class LigneProduction(BaseModel):
    production = models.ForeignKey(Production, on_delete = models.CASCADE, related_name="production_ligne")
    brique     = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_ligneproduction")
    perte      = models.IntegerField(default=0)
    quantite   = models.IntegerField(default=0)


class ConsommationJour(BaseModel):
    date        = models.DateField(default="")
    comment     = models.TextField(default="")
    utilisateur = models.ForeignKey(Utilisateur,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_consommationjour")


class LigneConsommation(BaseModel):
    production = models.ForeignKey(Production, on_delete = models.CASCADE, related_name="production_ligneconsommation")
    ressource  = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_ligneconsommation")
    quantite   = models.IntegerField(default = 0)



class ExigenceProduction(BaseModel):
    brique   = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_exigenceproduction")
    quantite = models.IntegerField(default=0)


class LigneExigenceProduction(BaseModel):
    exigence  = models.ForeignKey(ExigenceProduction, on_delete = models.CASCADE, related_name="agence_acces")
    ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="agence_acces")
    quantite  = models.IntegerField(default = 0)



class InitialBriqueAgence(BaseModel):
    agence   = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_initialbrique")
    brique   = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_initialagence")
    quantite = models.IntegerField(default=0)


class InitialRessourceAgence(BaseModel):
    agence    = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_initialressource")
    ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_initialagence")
    quantite  = models.IntegerField(default=0)



class PerteRessource(BaseModel):
    type        = models.ForeignKey(TypePerte, on_delete = models.CASCADE, related_name="type_perte")
    agence      = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_perteressource")
    ressource   = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_perte")
    utilisateur = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, related_name="utilisateur_perte")
    etat        = models.ForeignKey(Etat, on_delete = models.CASCADE)
    quantite    = models.IntegerField(default=0)
    comment     = models.IntegerField(default=0)


class PerteBrique(BaseModel):
    type        = models.ForeignKey(TypePerte, on_delete = models.CASCADE, related_name="agence_acces")
    agence      = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    brique      = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="agence_acces")
    utilisateur = models.ForeignKey(Utilisateur,  null = True, blank=True, on_delete = models.CASCADE, related_name="utilisateur_acces")
    etat        = models.ForeignKey(Etat, on_delete = models.CASCADE, related_name="agence_acces")
    quantite    = models.IntegerField(default=0)
    comment     = models.IntegerField(default=0)


class LignePerteBrique(BaseModel):
    perte    = models.ForeignKey(PerteBrique, on_delete = models.CASCADE, related_name="perte_ligne")
    brique   = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_perteligne")
    quantite = models.IntegerField(default=0)




class LigneTransfertStock(BaseModel):
    transfert      = models.ForeignKey(TransfertStock, on_delete = models.CASCADE, related_name="transfert_ligne")
    brique         = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_transfertligne")
    quantite_avant = models.IntegerField(default=0)
    quantite_apres = models.IntegerField(default=0)


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