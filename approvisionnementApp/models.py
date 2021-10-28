
from django.db import models
from commandeApp.models import Commande
from comptabilityApp.models import ReglementAchatStock, ReglementApprovisionnement, TypeMouvement
from django.db.models import Avg, Sum
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from coreApp.models import BaseModel, Etat
from ficheApp.views import achatstock

# Create your models here.


class Fournisseur(BaseModel):
    fullname        = models.CharField(max_length = 255)
    agence          = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_fournisseur")
    adresse         = models.CharField(max_length = 255, null = True, blank=True)
    email           = models.CharField(max_length = 255, null = True, blank=True)
    contact         = models.CharField(max_length = 255, null = True, blank=True)
    description     = models.TextField(default="",  null = True, blank=True)
    acompte_initial = models.IntegerField(default=0)
    dette_initial   = models.IntegerField(default=0)
    image          = models.ImageField(upload_to = "storage/images/fournisseurs/", max_length=255, null=True, blank=True)

    def __str__(self):
        return self.fullname

    def name(self):
        return self.fullname


    def acompte_actuel(self):
        total = 0
        datas = self.fournisseur_compte.filter(mouvement__type__etiquette = TypeMouvement.ENTREE).aggregate(Sum("mouvement__montant"))
        total += datas["mouvement__montant__sum"] or 0
        datas = self.fournisseur_compte.filter(mouvement__type__etiquette = TypeMouvement.SORTIE).aggregate(Sum("mouvement__montant"))
        total -= datas["mouvement__montant__sum"] or 0
        return self.acompte_initial + total


    def dette_totale(self):
        total = 0
        for appro in self.fournisseur_approvisionnement.filter(deleted = False).exclude(etat__etiquette = Etat.ANNULE):
            total += appro.reste_a_payer()

        datas = self.fournisseur_compte.filter(is_dette = True, mouvement__type__etiquette = TypeMouvement.SORTIE).aggregate(Sum("mouvement__montant"))
        total -= datas["mouvement__montant__sum"] or 0
        return self.dette_initial + total


class AchatStock(BaseModel):
    reference         = models.CharField(max_length = 255)
    agence            = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_achatstock")
    montant           = models.IntegerField(default = 0)
    avance            = models.IntegerField(default = 0)    
    reste             = models.IntegerField(default = 0)    
    transport          = models.IntegerField(default = 0)
    fournisseur       = models.ForeignKey(Fournisseur, on_delete = models.CASCADE, related_name="fournisseur_achatstock")
    etat              = models.ForeignKey("coreApp.Etat",  on_delete = models.CASCADE) 
    employe           = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_achatstock")
    employe_reception = models.ForeignKey("organisationApp.Employe", null = True, blank=True,  on_delete = models.CASCADE, related_name="employe_reception_achatstock")
    comment           = models.TextField(default="",  null = True, blank=True);
    datelivraison     = models.DateTimeField(null = True, blank=True)

    def reste_a_payer(self):
        data = ReglementAchatStock.objects.filter(achatstock = self).aggregate(Sum("mouvement__montant"))
        return self.montant - (data["mouvement__montant__sum"] or 0)

class LigneAchatStock(BaseModel):
    achatstock    = models.ForeignKey(AchatStock, on_delete = models.CASCADE, related_name="achatstock_ligne")
    brique        = models.ForeignKey("productionApp.Brique", on_delete = models.CASCADE, related_name="brique_ligneachatstock")
    quantite      = models.IntegerField(default = 0)
    quantite_recu = models.IntegerField(default = 0)
    price         = models.IntegerField(default = 0)




class Approvisionnement(BaseModel):
    reference          = models.CharField(max_length = 255)
    montant            = models.IntegerField(default = 0)
    avance             = models.IntegerField(default = 0)
    reste              = models.IntegerField(default = 0)
    transport          = models.IntegerField(default = 0)
    fournisseur        = models.ForeignKey(Fournisseur, on_delete = models.CASCADE, related_name="fournisseur_approvisionnement");
    agence             = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_approvisionnement")
    employe            = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_approvisionnement")
    employe_reception  = models.ForeignKey("organisationApp.Employe",  null = True, blank=True, on_delete = models.CASCADE, related_name="employe_reception_approvisionnement")
    etat               = models.ForeignKey("coreApp.Etat", on_delete = models.CASCADE) 
    comment            = models.TextField(default="",  null = True, blank=True);
    datelivraison      = models.DateTimeField(null = True, blank=True,);

    acompteFournisseur = models.IntegerField(default = 0)
    detteFournisseur   = models.IntegerField(default = 0)

    def __str__(self):
        return "Approvisionnement N°"+str(self.id)

    
    def reste_a_payer(self):
        data = ReglementApprovisionnement.objects.filter(approvisionnement = self).aggregate(Sum("mouvement__montant"))
        return self.montant - (data["mouvement__montant__sum"] or 0)


class LigneApprovisionnement(BaseModel):
    approvisionnement = models.ForeignKey(Approvisionnement, on_delete = models.CASCADE, related_name="approvisionnement_ligne")
    ressource         = models.ForeignKey("productionApp.Ressource", on_delete = models.CASCADE, related_name="ressource_ligneapprovisionnement")
    quantite          = models.IntegerField(default = 0)
    quantite_recu     = models.IntegerField(default = 0)
    price             = models.IntegerField(default = 0)




######################################################################################################
##### SIGNAUX


@receiver(pre_save, sender = LigneAchatStock)
@receiver(pre_save, sender = LigneApprovisionnement)
def pre_save_ligne_appro(sender, instance, **kwargs):
    if instance._state.adding:
        instance.quantite_recu = instance.quantite