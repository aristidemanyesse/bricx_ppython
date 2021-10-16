from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import datetime, pytz
from django.db.models import Sum, Avg

from coreApp.models import BaseModel, Etat
from productionApp.models import Brique
from livraisonApp.models import LigneLivraison
from comptabilityApp.models import ReglementCommande
# Create your models here.


class ZoneLivraison(BaseModel):
    name   = models.CharField(max_length = 255)
    agence = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_zone")



class PrixZoneLivraison(BaseModel):
    zone   = models.ForeignKey(ZoneLivraison, on_delete = models.CASCADE, related_name="zone_prix") 
    brique = models.ForeignKey("productionApp.Brique", on_delete = models.CASCADE, related_name="brique_zoneprix") 
    price  = models.IntegerField(default=0)

    def __str__(self):
        return "Prix de livraison de "+self.brique.name+" à " +self.zone.name




class GroupeCommande(BaseModel):
    client = models.ForeignKey("clientApp.Client", on_delete = models.CASCADE, related_name="client_groupecommande")
    agence = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_groupecommande")
    etat   = models.ForeignKey("coreApp.Etat", on_delete = models.CASCADE)
    datelivraison      = models.DateTimeField(null = True, blank=True,)


    def reste(self, brique):
        annule = Etat.objects.get(etiquette = Etat.ANNULE)
        commades = LigneCommande.objects.filter(commande__groupecommande = self, commande__deleted = False, brique = brique).aggregate(Sum("quantite"))
        livraisons = LigneLivraison.objects.filter(livraison__groupecommande = self, brique = brique).exclude(livraison__etat__etiquette = Etat.ANNULE).aggregate(Sum("quantite"))
        return (commades["quantite__sum"] or 0) - (livraisons["quantite__sum"] or 0)


    def reste_a_payer(self):
        total = 0
        for commande in self.commande_groupecommande.filter(deleted = False):
            total += commande.reste_a_payer()
        return total


    def all_briques(self):
        briques = {}
        for brique in Brique.objects.filter(active = True, deleted = False):
            count =  self.reste(brique)
            if count > 0:
                briques[brique] = count
        return briques


    def __str__(self):
        return "Groupe de commande de "+self.client.name




class Commande(BaseModel):
    reference          = models.CharField(max_length = 255)
    groupecommande     = models.ForeignKey(GroupeCommande, on_delete = models.CASCADE, related_name="commande_groupecommande")
    agence             = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_commande")
    zonelivraison      = models.ForeignKey(ZoneLivraison, on_delete = models.CASCADE, related_name="zone_commande")
    lieu               = models.CharField(max_length = 255)
    montant            = models.IntegerField(default = 0)
    avance             = models.IntegerField(default = 0)
    taux_tva           = models.IntegerField(default = 0)
    tva                = models.IntegerField(default = 0)
    employe            = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_commande")
    comment            = models.TextField(default="");

    datelivraison      = models.DateTimeField(null = True, blank=True,)
    acompteFournisseur = models.IntegerField(default = 0)
    detteFournisseur   = models.IntegerField(default = 0)

    def reste_a_payer(self):
        data = ReglementCommande.objects.filter(commande = self).aggregate(Sum("reglement__mouvement__montant"))
        return self.montant - (data["reglement__mouvement__montant__sum"] or 0)
    

    def all_briques(self):
        briques = {}
        for brique in Brique.objects.filter(active = True, deleted = False):
            ligne = LigneCommande.objects.filter(commande = self, commande__deleted = False, brique = brique).first()
            briques[brique] = ligne.quantite if ligne != None else 0
        return briques



    def __str__(self):
        return "Commande N°"+self.reference






class LigneCommande(BaseModel):
    commande = models.ForeignKey(Commande, on_delete = models.CASCADE, related_name="commande_ligne")
    brique   = models.ForeignKey("productionApp.Brique", on_delete = models.CASCADE, related_name="brique_lignecommande")
    quantite = models.IntegerField(default = 0)
    price    = models.IntegerField(default = 0)


    def __str__(self):
        return str(self.quantite) + " " +self.brique.name+" à " +str(self.price)



######################################################################################################
##### SIGNAUX



@receiver(post_save, sender = ZoneLivraison)
def post_save_zone_livraison(sender, instance, created, **kwargs):
    if created:
        for brique in "productionApp.Brique".objects.filter(deleted = False):
            PrixZoneLivraison.objects.create(
                brique = brique,
                zone = instance,
                price = 0
            )


@receiver(post_save, sender = "productionApp.Brique")
def post_save_brique(sender, instance, created, **kwargs):
    if created:
        for zone in ZoneLivraison.objects.filter(deleted = False):
            PrixZoneLivraison.objects.create(
                brique = instance,
                zone = zone,
                price = 0
            )


@receiver(post_save, sender = Commande)
def post_save_commande(sender, instance, created, **kwargs):
    date =  instance.groupecommande.datelivraison.replace(tzinfo=None)
    if date is None or date < datetime.datetime.now():
        if instance.groupecommande.datelivraison is None or instance.groupecommande.datelivraison < instance.commande:
            instance.groupecommande.datelivraison = instance.datelivraison
            instance.groupecommande.save()