
from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from comptabilityApp.models import ReglementTricycle

from coreApp.models import BaseModel, Etat
import datetime, uuid

from productionApp.models import Brique
# Create your models here.

class ModeLivraison(BaseModel):
    DEFAUT = "1"
    TRICYCLE = "2"
    CLIENT = "3"

    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)

    class Meta:
        ordering = ['etiquette']


class Chauffeur(BaseModel):
    agence         = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_chauffeur")
    name = models.CharField(max_length = 255)
    adresse  = models.CharField(max_length = 255, null = True, blank=True)
    contact  = models.CharField(max_length = 255, null = True, blank=True)



class Vehicule(BaseModel):
    agence         = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_vehicule")
    immatriculation = models.CharField(max_length = 255)
    modele          = models.CharField(max_length = 255, null = True, blank=True)

    def __str__(self):
        return self.modele+" | "+self.immatriculation

    def name(self):
        return self.modele+" | "+self.immatriculation


class Livraison(BaseModel):
    reference      = models.CharField(max_length = 255)
    groupecommande = models.ForeignKey("commandeApp.GroupeCommande", on_delete = models.CASCADE, related_name="groupecommande_livraison")
    agence         = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_livraison")
    modelivraison  = models.ForeignKey(ModeLivraison, on_delete = models.CASCADE, related_name="mode_livraison")
    zone           = models.ForeignKey("commandeApp.ZoneLivraison", on_delete = models.CASCADE, related_name="zone_livraison")
    lieu           = models.CharField(max_length = 255)
    employe        = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_livraison")
    chauffeur      = models.ForeignKey(Chauffeur, on_delete = models.CASCADE, null=True, blank=True, related_name="chauffeur_livraison")
    vehicule       = models.ForeignKey(Vehicule, on_delete = models.CASCADE, null=True, blank=True, related_name="vehicule_livraison")
    etat           = models.ForeignKey("coreApp.Etat",  on_delete = models.CASCADE) 
    comment        = models.TextField(default="",  null = True, blank=True);

    datelivraison          = models.DateTimeField(null = True, blank=True)
    nom_receptionniste     = models.CharField(max_length = 255, default="", null = True, blank=True)
    contact_receptionniste = models.CharField(max_length = 255, default="", null = True, blank=True)
    chargement             = models.BooleanField(default=True)
    dechargement           = models.BooleanField(default=True)

    class Meta:
        ordering = ['etat__etiquette', "-created_at"]

    def __str__(self):
        return "Livraison N°"+self.reference


    def all_briques(self):
        briques = {}
        for brique in Brique.objects.filter(active = True, deleted = False):
            ligne = LigneLivraison.objects.filter(livraison = self, livraison__deleted = False, brique = brique).first()
            briques[brique] = "-"
            if ligne != None:
                briques[brique] = ligne.quantite if ligne.livraison.etat.etiquette == str(Etat.EN_COURS) else ligne.livree
        return briques


class LigneLivraison(BaseModel):
    livraison = models.ForeignKey(Livraison, on_delete = models.CASCADE, related_name="livraison_ligne")
    brique    = models.ForeignKey("productionApp.Brique", on_delete = models.CASCADE, related_name="brique_lignelivraison")
    quantite  = models.IntegerField(default = 0)
    livree  = models.IntegerField(default = 0)
    surplus   = models.IntegerField(default = 0)
    perte     = models.IntegerField(default = 0)
    reste     = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.quantite) + " " +self.brique.name


class Tricycle(BaseModel):
    livraison = models.ForeignKey(Livraison, on_delete = models.CASCADE, related_name="livraison_tricycle")
    montant   = models.IntegerField(default = 0)
    fullname  = models.CharField(max_length = 255)
    contact   = models.CharField(max_length = 255, null = True, blank=True)

    def __str__(self):
        return self.fullname


    def reste_a_payer(self):
        data = ReglementTricycle.objects.filter(tricycle = self).aggregate(Sum("mouvement__montant"))
        return self.montant - (data["mouvement__montant__sum"] or 0)

######################################################################################################
##### SIGNAUX




@receiver(pre_save, sender = Livraison)
def pre_save_livraison(sender, instance, **kwargs):
    if instance._state.adding:
        if instance.lieu == "":
            raise Exception("Veuillez préciser le lieu exact de la livraison !")
        instance.reference = uuid.uuid4()
        instance.etat = Etat.objects.get(etiquette = Etat.EN_COURS)



@receiver(pre_save, sender = LigneLivraison)
def pre_save_ligne_livraison(sender, instance, **kwargs):
    if instance._state.adding:
        instance.livree = instance.quantite