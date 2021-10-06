from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import datetime, pytz
import productionApp.models as production_models
import organisationApp.models as organisation_models
import clientApp.models as client_models
import coreApp.models as core_models
import comptabilityApp.models as comptability_models
# Create your models here.


class ZoneLivraison(core_models.BaseModel):
    name   = models.CharField(max_length = 255)
    agence = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_zone")



class PrixZoneLivraison(core_models.BaseModel):
    zone   = models.ForeignKey(ZoneLivraison, on_delete = models.CASCADE, related_name="zone_prix") 
    brique = models.ForeignKey(production_models.Brique, on_delete = models.CASCADE, related_name="brique_zoneprix") 
    price  = models.IntegerField(default=0)

    def __str__(self):
        return "Prix de livraison de "+self.brique.name+" à " +self.zone.name




class GroupeCommande(core_models.BaseModel):
    client = models.ForeignKey(client_models.Client, on_delete = models.CASCADE, related_name="client_groupecommande")
    agence = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_groupecommande")
    etat   = models.ForeignKey(core_models.Etat, on_delete = models.CASCADE)
    datelivraison      = models.DateTimeField(null = True, blank=True,)

    def reste_a_payer(self):
        total = 0
        for commande in self.commande_groupecommande.filter(etat__etiquette = core_models.Etat.EN_COURS):
            total += commande.reste_a_payer()
        return total


    def __str__(self):
        return "Groupe de commande de "+self.client.name




class Commande(core_models.BaseModel):
    reference          = models.CharField(max_length = 255)
    groupecommande     = models.ForeignKey(GroupeCommande, on_delete = models.CASCADE, related_name="commande_groupecommande")
    agence             = models.ForeignKey(organisation_models.Agence, on_delete = models.CASCADE, related_name="agence_commande")
    zonelivraison      = models.ForeignKey(ZoneLivraison, on_delete = models.CASCADE, related_name="zone_commande")
    lieu               = models.CharField(max_length = 255)
    montant            = models.IntegerField(default = 0)
    avance             = models.IntegerField(default = 0)
    taux_tva           = models.IntegerField(default = 0)
    tva                = models.IntegerField(default = 0)
    employe            = models.ForeignKey(organisation_models.Employe, on_delete = models.CASCADE, related_name="employe_commande")
    etat               = models.ForeignKey(core_models.Etat, on_delete = models.CASCADE) 
    comment            = models.TextField(default="");

    datelivraison      = models.DateTimeField(null = True, blank=True,)
    acompteFournisseur = models.IntegerField(default = 0)
    detteFournisseur   = models.IntegerField(default = 0)

    def reste_a_payer(self):
        data = comptability_models.ReglementCommande.objects.filter().aggregate(Sum("montant"))
        return self.montant - data["montant__sum"] or 0
    


    def __str__(self):
        return "Commande N°"+self.reference



class LigneCommande(core_models.BaseModel):
    commande = models.ForeignKey(Commande, on_delete = models.CASCADE, related_name="commande_ligne")
    brique   = models.ForeignKey(production_models.Brique, on_delete = models.CASCADE, related_name="brique_lignecommande")
    quantite = models.IntegerField(default = 0)
    price    = models.IntegerField(default = 0)






######################################################################################################
##### SIGNAUX



@receiver(post_save, sender = ZoneLivraison)
def post_save_zone_livraison(sender, instance, created, **kwargs):
    if created:
        for brique in production_models.Brique.objects.filter(deleted = False):
            PrixZoneLivraison.objects.create(
                brique = brique,
                zone = instance,
                price = 0
            )


@receiver(post_save, sender = production_models.Brique)
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