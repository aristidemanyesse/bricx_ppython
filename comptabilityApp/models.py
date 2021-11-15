
from django.db import models

from coreApp.models import BaseModel, MyCodeException
from django.db import models, transaction
import uuid, datetime, json, random
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Sum
import math
# Create your models here.

class TypeOperationCaisse(BaseModel):
    DEPOT = "1"
    RETRAIT = "-1"

    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)


class TypeMouvement(BaseModel):
    DEPOT = "1"
    RETRAIT = "-1"

    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)


class CategoryOperation(BaseModel):
    REFUND_FOURNISSEUR = 1
    TRANSFERT_DEPOT    = 2

    MAIN_D_OEUVRE        = 10
    REFUND_CLIENT      = 11
    TRANSPORT          = 12
    TRANSFERT_RETRAIT  = 13

    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)
    type      = models.ForeignKey(TypeOperationCaisse, on_delete = models.CASCADE, related_name="type_categorie")
    color     = models.CharField(default="", max_length = 255,  null = True, blank=True)


class ModePayement(BaseModel):
    ESPECES      = "1"
    PRELEVEMENT  = "2"

    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)
    etat      = models.ForeignKey("coreApp.Etat", on_delete = models.CASCADE)
    class Meta:
        ordering = ['etiquette']

class Compte(BaseModel):
    name           = models.CharField(max_length = 255)
    initial_amount = models.IntegerField(default=0)
    etablissement  = models.CharField(max_length = 255, default="", null = True, blank=True)
    numero         = models.CharField(max_length = 255, default="", null = True, blank=True)
    agence = models.ForeignKey("organisationApp.Agence", null=True, blank=True, on_delete = models.CASCADE, related_name="agence_compte")

    def __str__(self):
        return self.name

    def total_entree(self, debut = None, fin = None):
        debut = debut or datetime.date.fromisoformat("2021-11-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        total =  self.compte_mouvement.filter(deleted=False, type__etiquette = TypeMouvement.DEPOT, created_at__range = (debut, fin)).exclude(mode__etiquette = ModePayement.PRELEVEMENT).aggregate(Sum('montant'))
        return (total["montant__sum"] or 0)

    def total_sortie(self, debut = None, fin = None):
        debut = debut or datetime.date.fromisoformat("2021-11-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        total =  self.compte_mouvement.filter(deleted=False, type__etiquette = TypeMouvement.RETRAIT, created_at__range = (debut, fin)).exclude(mode__etiquette = ModePayement.PRELEVEMENT).aggregate(Sum('montant'))
        return (total["montant__sum"] or 0)

    def solde_actuel(self, fin = None):
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        return self.initial_amount + self.total_entree(None, fin) - self.total_sortie(None, fin)


    def stats(self, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-11-01")
        fin = fin or datetime.date.today()
        tableaux = []
        delta = fin - debut
        nb = math.ceil(delta.days / 12)
        index = debut
        while index <= fin :
            debut = index
            index_fin = index + datetime.timedelta(days=nb)

            data = {}
            data["year"] = index.year
            data["month"] = index.month
            data["day"] = index.day
            data["nb"] = nb

            data["sortie"] = self.total_sortie(debut, index_fin)
            data["entree"] = self.total_entree(debut, index_fin)
            data["solde"] = self.solde_actuel(index_fin)

            tableaux.append(data)
            index = index_fin

        return tableaux


class Mouvement(BaseModel):
    name      = models.CharField(max_length = 255)
    type      = models.ForeignKey(TypeMouvement,  on_delete = models.CASCADE, related_name="type_mouvement")
    reference = models.CharField(max_length = 255, null = True, blank=True)
    montant   = models.IntegerField(default=0)
    compte    = models.ForeignKey(Compte, on_delete = models.CASCADE, related_name="compte_mouvement")
    employe   = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_payetricycle")
    etat      = models.ForeignKey("coreApp.Etat",  null = True, blank=True, on_delete = models.CASCADE)
    date_approbation = models.DateTimeField(null = True, blank=True)
    mode      = models.ForeignKey(ModePayement,  null = True, blank=True, on_delete = models.CASCADE, related_name="modepayement_mouvement")
    structure = models.CharField(default=0, max_length = 255, null = True, blank=True)
    numero    = models.CharField(default=0, max_length = 255, null = True, blank=True)
    comment   = models.TextField(default="",  null = True, blank=True)

    class Meta:
        ordering = ["created_at"]


class ReglementApprovisionnement(BaseModel):
    mouvement    = models.ForeignKey(Mouvement, on_delete = models.CASCADE, related_name="mouvement_reglement_appro")
    approvisionnement = models.ForeignKey("approvisionnementApp.Approvisionnement", on_delete = models.CASCADE, related_name="approvisionnement_reglement")
    restait  = models.IntegerField(default=0,  null = True, blank=True)

    def __str__(self):
        return self.mouvement.reference

class ReglementCommande(BaseModel):
    mouvement    = models.ForeignKey(Mouvement, on_delete = models.CASCADE, related_name="mouvement_reglement_commande")
    commande  = models.ForeignKey("commandeApp.Commande", on_delete = models.CASCADE, related_name="commande_reglement")
    restait  = models.IntegerField(default=0,  null = True, blank=True)

    def __str__(self):
        return self.mouvement.reference

    
    @staticmethod
    def total(agence, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-11-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        total = ReglementCommande.objects.filter(deleted = False, mouvement__compte__agence = agence, created_at__range = (debut, fin)).aggregate(Sum('mouvement__montant'))
        return total["mouvement__montant__sum"] or 0


class CompteClient(BaseModel):
    mouvement    = models.ForeignKey(Mouvement, on_delete = models.CASCADE, related_name="mouvement_compteclient")
    client  = models.ForeignKey("clientApp.Client", on_delete = models.CASCADE, related_name="client_compte")
    is_dette = models.BooleanField(default=False)

    def __str__(self):
        return self.client.name +" | "+self.mouvement.reference



class CompteFournisseur(BaseModel):
    mouvement    = models.ForeignKey(Mouvement, on_delete = models.CASCADE, related_name="mouvement_comptefournisseur")
    fournisseur  = models.ForeignKey("approvisionnementApp.Fournisseur", on_delete = models.CASCADE, related_name="fournisseur_compte")
    is_dette = models.BooleanField(default=False)

    def __str__(self):
        return self.fournisseur.fullname +" | "+self.mouvement.reference


class ReglementAchatStock(BaseModel):
    mouvement    = models.ForeignKey(Mouvement, on_delete = models.CASCADE, related_name="mouvement_reglement_achatstock")
    achatstock = models.ForeignKey("approvisionnementApp.AchatStock", on_delete = models.CASCADE, related_name="achatstock_reglement")
    restait  = models.IntegerField(default=0)

    def __str__(self):
        return self.mouvement.reference

class ReglementTricycle(BaseModel):
    mouvement    = models.ForeignKey(Mouvement, on_delete = models.CASCADE, related_name="mouvement_reglement")
    tricycle = models.ForeignKey("livraisonApp.Tricycle", on_delete = models.CASCADE, related_name="tricycle_reglement")
    restait  = models.IntegerField(default=0)

    def __str__(self):
        return self.mouvement.reference

class Operation(BaseModel):
    category         = models.ForeignKey(CategoryOperation,  null = True, blank=True, on_delete = models.CASCADE, related_name="category_operation")
    mouvement        = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="mouvement_operation")
    etat             = models.ForeignKey("coreApp.Etat",  null = True, blank=True, on_delete = models.CASCADE)
    image            = models.ImageField(max_length = 255, upload_to = "images/operations/", default="", null = True, blank=True)

    def __str__(self):
        return self.category.name +" | "+self.mouvement.reference

class Transfertfond(BaseModel):
    reference          = models.CharField(max_length = 255)
    montant            = models.IntegerField(default=0)
    compte_source      = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_source_transfert")
    compte_destination = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_destination_transfert")
    etat               = models.ForeignKey("coreApp.Etat",  null = True, blank=True, on_delete = models.CASCADE)
    employe            = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_transfertfond")
    comment            = models.TextField(default="",  null = True, blank=True)

    def __str__(self):
        return str(self.reference)



############################################################################################################################:

@receiver(pre_save, sender = Mouvement)
def pre_save_mouvement(sender, instance, **kwargs):
    if int(instance.montant) > 0:
        if instance._state.adding:
            instance.reference = uuid.uuid4()
            instance.etat = instance.mode.etat
    else:   
        #verifie si l'invité n'a pas deja un compte
        raise Exception(MyCodeException.INCORRECT_MONTANT)
    


@receiver(pre_save, sender = ReglementCommande)
def pre_save_reglement_commande(sender, instance, **kwargs):
    if instance._state.adding:
        instance.restait = instance.commande.reste_a_payer() - instance.mouvement.montant


@receiver(post_save, sender = ReglementCommande)
def post_save_reglement_commande(sender, instance, created, **kwargs):
    if created:
        instance.restait = instance.commande.reste_a_payer()
        if instance.mouvement.mode.etiquette == ModePayement.PRELEVEMENT:
            CompteClient.objects.create(
                client = instance.commande.groupecommande.client,
                mouvement = instance.mouvement
            )




@receiver(pre_save, sender = ReglementApprovisionnement)
def pre_save_reglement_approvisionnement(sender, instance, **kwargs):
    if instance._state.adding:
        instance.restait = instance.approvisionnement.reste_a_payer() - instance.mouvement.montant


@receiver(post_save, sender = ReglementApprovisionnement)
def post_save_reglement_approvisionnement(sender, instance, created, **kwargs):
    if created:
        instance.restait = instance.approvisionnement.reste_a_payer()
        if instance.mouvement.mode.etiquette == ModePayement.PRELEVEMENT:
            CompteFournisseur.objects.create(
                fournisseur = instance.approvisionnement.fournisseur,
                mouvement = instance.mouvement,
            )



@receiver(pre_save, sender = ReglementAchatStock)
def pre_save_reglement_achatstock(sender, instance, **kwargs):
    if instance._state.adding:
        instance.restait = instance.achatstock.reste_a_payer() - instance.mouvement.montant


@receiver(post_save, sender = ReglementAchatStock)
def post_save_reglement_achatstock(sender, instance, created, **kwargs):
    if created:
        if instance.mouvement.mode.etiquette == ModePayement.PRELEVEMENT:
            CompteFournisseur.objects.create(
                fournisseur = instance.achatstock.fournisseur,
                mouvement = instance.mouvement
            )



@receiver(pre_save, sender = Operation)
def pre_save_operation(sender, instance, **kwargs):
    if instance._state.adding:
            instance.etat = instance.mouvement.mode.etat


# @receiver(post_save, sender = Mouvement)
# def post_save_forgotpasswor(sender, created, instance, **kwargs):
#     if created :
#         SendMail.send_mail(Utilisateur, instance.email, SendMail.CHANGING_PASSWORD_MAIL, demande_id = instance.id)





