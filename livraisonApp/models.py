
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver

from coreApp.models import BaseModel, Etat
import datetime, uuid
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
    name = models.CharField(max_length = 255)
    adresse  = models.CharField(max_length = 255, null = True, blank=True)
    contact  = models.CharField(max_length = 255, null = True, blank=True)
    etat     = models.ForeignKey("coreApp.Etat", on_delete = models.CASCADE) 



class Vehicule(BaseModel):
    immatriculation = models.CharField(max_length = 255)
    modele          = models.CharField(max_length = 255, null = True, blank=True)
    marque          = models.CharField(max_length = 255, null = True, blank=True)
    etat            = models.ForeignKey("coreApp.Etat",  on_delete = models.CASCADE) 

    def __str__(self):
        return self.marque +" "+self.modele+" | "+self.immatriculation

    def name(self):
        return self.marque +" "+self.modele+" | "+self.immatriculation


class Livraison(BaseModel):
    reference      = models.CharField(max_length = 255)
    groupecommande = models.ForeignKey("commandeApp.GroupeCommande", on_delete = models.CASCADE, related_name="groupecommande_livraison")
    agence         = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_livraison")
    modelivraison  = models.ForeignKey(ModeLivraison, on_delete = models.CASCADE, related_name="mode_livraison")
    lieu           = models.CharField(max_length = 255)
    employe        = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_livraison")
    chauffeur      = models.ForeignKey(Chauffeur, on_delete = models.CASCADE, null=True, blank=True, related_name="chauffeur_livraison")
    vehicule       = models.ForeignKey(Vehicule, on_delete = models.CASCADE, null=True, blank=True, related_name="vehicule_livraison")
    etat           = models.ForeignKey("coreApp.Etat",  on_delete = models.CASCADE) 
    comment        = models.TextField(default="");

    datelivraison          = models.DateTimeField(null = True, blank=True)
    nom_receptionniste     = models.CharField(max_length = 255, default="")
    contact_receptionniste = models.CharField(max_length = 255, default="")
    chargement             = models.BooleanField(default=True)
    dechargement           = models.BooleanField(default=True)

    def __str__(self):
        return "Livraison N°"+self.reference

class LigneLivraison(BaseModel):
    livraison = models.ForeignKey(Livraison, on_delete = models.CASCADE, related_name="livraison_ligne")
    brique    = models.ForeignKey("productionApp.Brique", on_delete = models.CASCADE, related_name="brique_lignelivraison")
    quantite  = models.IntegerField(default = 0)
    surplus   = models.IntegerField(default = 0)
    perte     = models.IntegerField(default = 0)
    reste     = models.IntegerField(default = 0)




class Tricycle(BaseModel):
    livraison = models.ForeignKey(Livraison, on_delete = models.CASCADE, related_name="livraison_tricycle")
    montant   = models.IntegerField(default = 0)
    fullname  = models.CharField(max_length = 255)
    adresse   = models.CharField(max_length = 255, null = True, blank=True)
    contact   = models.CharField(max_length = 255, null = True, blank=True)
    etat      = models.ForeignKey("coreApp.Etat",  on_delete = models.CASCADE) 



######################################################################################################
##### SIGNAUX




@receiver(pre_save, sender = Livraison)
def pre_save_commande(sender, instance, **kwargs):
    print(datetime.datetime.now().date())
    if instance.datelivraison is None:
        raise Exception("Veuillez notifier une date correcte de livraison pour la commande")
    if instance.lieu == "":
        raise Exception("Veuillez préciser le lieu exact de la livraison !")
    instance.reference = uuid.uuid4()
    instance.etat = Etat.objects.get(etiquette = Etat.EN_COURS)