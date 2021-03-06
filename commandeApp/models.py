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
        return _("Prix de livraison de ")+self.brique.name+" à " +self.zone.name




class GroupeCommande(BaseModel):
    client = models.ForeignKey("clientApp.Client", on_delete = models.CASCADE, related_name="client_groupecommande")
    agence = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_groupecommande")
    etat   = models.ForeignKey("coreApp.Etat", on_delete = models.CASCADE)
    datelivraison      = models.DateTimeField(null = True, blank=True,)

    def reste(self, brique):
        commades = LigneCommande.objects.filter(commande__groupecommande = self, commande__deleted = False, brique = brique).aggregate(Sum("quantite"))
        livraisons = LigneLivraison.objects.filter(livraison__groupecommande = self, brique = brique).exclude(livraison__etat__etiquette = Etat.ANNULE).aggregate(Sum("livree"))
        return (commades["quantite__sum"] or 0) - (livraisons["livree__sum"] or 0)

    def reste_a_payer(self):
        total = 0
        for commande in self.commande_groupecommande.filter(deleted = False):
            total += commande.reste_a_payer()
        return total
    
    
    def all_briques_all(self):
        briques = {}
        for brique in Brique.objects.filter(active = True, deleted = False):
            count =  self.reste(brique)
            briques[brique] = count
        return briques

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

    @staticmethod
    def maj_etat():
        try:
            groupes = GroupeCommande.objects.filter(etat__etiquette = Etat.EN_COURS, deleted = False)
            for groupe in groupes:
                if len(groupe.all_briques()) == 0:
                    groupe.etat = Etat.objects.get(etiquette = Etat.TERMINE)
                    groupe.save()
        except Exception as e:
            print("Erreur groupe commande ", e)
                


    def __str__(self):
        return _("Groupe de commande de ")+self.client.name




class Commande(BaseModel):
    groupecommande = models.ForeignKey(GroupeCommande, on_delete = models.CASCADE, related_name="commande_groupecommande")
    agence         = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_commande")
    zone           = models.ForeignKey(ZoneLivraison, on_delete = models.CASCADE, related_name="zone_commande")
    lieu           = models.CharField(max_length = 255)
    montant        = models.FloatField(default = 0)
    avance         = models.FloatField(default = 0)
    taux_tva       = models.FloatField(default = 0)
    tva            = models.FloatField(default = 0)
    employe        = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_commande")
    comment        = models.TextField(default="",  null = True, blank=True);
    is_conversion      = models.BooleanField(default = False)

    datelivraison  = models.DateField(null = True, blank=True,)
    acompte_client = models.FloatField(default = 0)
    dette_client   = models.FloatField(default = 0)
    class Meta:
        ordering = ['deleted', "-created_at"]

    def reste_a_payer(self):
        data = ReglementCommande.objects.filter(commande = self, deleted =False).aggregate(Sum("mouvement__montant"))
        return self.montant - (data["mouvement__montant__sum"] or 0)
    

    def all_briques(self):
        briques = {}
        for brique in Brique.objects.filter(active = True, deleted = False):
            ligne = LigneCommande.objects.filter(commande = self, commande__deleted = False, brique = brique).first()
            briques[brique] = ligne.quantite if ligne != None else 0
        return briques

    @staticmethod
    def chiffre_affaire(agence):
        total = Commande.objects.filter(deleted = False, agence = agence).aggregate(Sum("montant"))
        return total["montant__sum"] or 0


    def __str__(self):
        return _("Commande N°")+str(self.id)



class LigneCommande(BaseModel):
    commande = models.ForeignKey(Commande, on_delete = models.CASCADE, related_name="commande_ligne")
    brique   = models.ForeignKey("productionApp.Brique", on_delete = models.CASCADE, related_name="brique_lignecommande")
    quantite = models.IntegerField(default = 0)
    price    = models.IntegerField(default = 0)


    def __str__(self):
        return str(self.quantite) + " " +self.brique.name+" à " +str(self.price)




class Conversion(BaseModel):
    agence             = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_conversion")
    groupecommande_old = models.ForeignKey(GroupeCommande, on_delete = models.CASCADE, related_name="old_groupecommande_conversion")
    groupecommande_new = models.ForeignKey(GroupeCommande, on_delete = models.CASCADE, related_name="new_groupecommande_conversion")
    employe        = models.ForeignKey("organisationApp.Employe",  null = True, blank=True, on_delete = models.CASCADE, related_name="employe_transfertstock")

    def __str__(self):
        return _("Conversion N°")+str(self.id)

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



@receiver(pre_save, sender = GroupeCommande)
def pre_save_groupe_commande(sender, instance, **kwargs):
    if instance._state.adding:
        instance.datelivraison = datetime.datetime.now()
        instance.etat = Etat.objects.get(etiquette = Etat.EN_COURS)



@receiver(pre_save, sender = Commande)
def pre_save_commande(sender, instance, **kwargs):
    if instance._state.adding:
        if instance.datelivraison is None:
            raise Exception("Veuillez notifier une date correcte de livraison pour la commande")
        if instance.lieu == "":
            raise Exception("Veuillez préciser le lieu exact de la livraison !")
        instance.etat = Etat.objects.get(etiquette = Etat.EN_COURS)



@receiver(post_save, sender = Commande)
def post_save_commande(sender, instance, created, **kwargs):
    pass
    # date =  instance.groupecommande.datelivraison.replace(tzinfo=None)
    # if date < datetime.datetime.now():
    #     if instance.groupecommande.datelivraison is None or instance.groupecommande.datelivraison < instance.datelivraison:
    #         instance.groupecommande.datelivraison = instance.datelivraison
    #         instance.groupecommande.save()