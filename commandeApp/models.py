from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import datetime, uuid
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

    def get_zones(self):
        tab = []
        for commande in self.commande_groupecommande.filter(deleted = False):
            if commande.zone not in tab : tab.append(commande.zone)
        return tab

    def __str__(self):
        return "Groupe de commande de "+self.client.name




class Commande(BaseModel):
    reference      = models.CharField(max_length = 255)
    groupecommande = models.ForeignKey(GroupeCommande, on_delete = models.CASCADE, related_name="commande_groupecommande")
    agence         = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_commande")
    zone           = models.ForeignKey(ZoneLivraison, on_delete = models.CASCADE, related_name="zone_commande")
    lieu           = models.CharField(max_length = 255)
    montant        = models.IntegerField(default = 0)
    avance         = models.IntegerField(default = 0)
    taux_tva       = models.IntegerField(default = 0)
    tva            = models.IntegerField(default = 0)
    employe        = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_commande")
    comment        = models.TextField(default="",  null = True, blank=True);

    datelivraison  = models.DateTimeField(null = True, blank=True,)
    acompte_client = models.IntegerField(default = 0)
    dette_client   = models.IntegerField(default = 0)

    def reste_a_payer(self):
        data = ReglementCommande.objects.filter(commande = self).aggregate(Sum("mouvement__montant"))
        return self.montant - (data["mouvement__montant__sum"] or 0)
    

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




class Conversion(BaseModel):
    reference          = models.CharField(max_length = 255)
    agence             = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_conversion")
    groupecommande_old = models.ForeignKey(GroupeCommande, on_delete = models.CASCADE, related_name="old_groupecommande_conversion")
    groupecommande_new = models.ForeignKey(GroupeCommande, on_delete = models.CASCADE, related_name="new_groupecommande_conversion")
    employe        = models.ForeignKey("organisationApp.Employe",  null = True, blank=True, on_delete = models.CASCADE, related_name="employe_transfertstock")

    def __str__(self):
        return "Conversion N°"+self.reference

class LigneConversion(BaseModel):
    conversion      = models.ForeignKey(Conversion, on_delete = models.CASCADE, related_name="conversion_ligne")
    brique         = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_conversionligne")
    quantite_avant = models.IntegerField(default=0)
    quantite_apres = models.IntegerField(default=0)

    def __str__(self):
        return str(self.quantite_avant) + " " +self.brique.name+" => " +str(self.quantite_apres)


######################################################################################################
##### SIGNAUX



@receiver(post_save, sender = ZoneLivraison)
def post_save_zone_livraison(sender, instance, created, **kwargs):
    if created:
        for brique in Brique.objects.filter(deleted = False):
            PrixZoneLivraison.objects.create(
                brique = brique,
                zone = instance,
                price = 0
            )


@receiver(post_save, sender = Brique)
def post_save_brique(sender, instance, created, **kwargs):
    if created:
        for zone in ZoneLivraison.objects.filter(deleted = False):
            PrixZoneLivraison.objects.create(
                brique = instance,
                zone = zone,
                price = 0
            )



@receiver(pre_save, sender = GroupeCommande)
def pre_save_groupe_commande(sender, instance, **kwargs):
    instance.datelivraison = datetime.datetime.now()
    instance.etat = Etat.objects.get(etiquette = Etat.EN_COURS)



@receiver(pre_save, sender = Commande)
def pre_save_commande(sender, instance, **kwargs):
    if instance.datelivraison is None:
        raise Exception("Veuillez notifier une date correcte de livraison pour la commande")
    if instance.lieu == "":
        raise Exception("Veuillez préciser le lieu exact de la livraison !")
    instance.reference = uuid.uuid4()
    instance.etat = Etat.objects.get(etiquette = Etat.EN_COURS)



@receiver(post_save, sender = Commande)
def post_save_commande(sender, instance, created, **kwargs):
    pass
    # date =  instance.groupecommande.datelivraison.replace(tzinfo=None)
    # if date < datetime.datetime.now():
    #     if instance.groupecommande.datelivraison is None or instance.groupecommande.datelivraison < instance.datelivraison:
    #         instance.groupecommande.datelivraison = instance.datelivraison
    #         instance.groupecommande.save()