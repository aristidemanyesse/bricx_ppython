
from django.db import models

from coreApp.models import BaseModel, MyCodeException
from django.db import models, transaction
import uuid, datetime, json, random
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Sum

# Create your models here.

class TypeOperationCaisse(BaseModel):
    ENTREE = "1"
    SORTIE = "-1"

    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)


class TypeMouvement(BaseModel):
    ENTREE = "1"
    SORTIE = "-1"

    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)


class TypeReglement(BaseModel):
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)


class CategoryOperation(BaseModel):
    REFUND_CLIENT = 5

    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255)
    type      = models.ForeignKey(TypeOperationCaisse, on_delete = models.CASCADE, related_name="type_categorie")
    color     = models.CharField(default="", max_length = 255,  null = True, blank=True)


class ModePayement(BaseModel):
    PRELEVEMENT  = "1"
    ESPECES      = "2"
    MOBILE_MONEY = "3"
    CHEQUE       = "4"

    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255)
    etat      = models.ForeignKey("coreApp.Etat", on_delete = models.CASCADE)
    class Meta:
        ordering = ['etiquette']

class Compte(BaseModel):
    name           = models.CharField(max_length = 255)
    initial_amount = models.IntegerField(default=0)
    etablissement  = models.CharField(max_length = 255, null = True, blank=True)
    numero         = models.CharField(max_length = 255, null = True, blank=True)
    agence = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_compte")

    def __str__(self):
        return self.name

    def solde_actuel(self):
        return 166132

class Mouvement(BaseModel):
    name      = models.CharField(max_length = 255)
    type      = models.ForeignKey(TypeMouvement,  on_delete = models.CASCADE, related_name="type_mouvement")
    reference = models.CharField(max_length = 255, null = True, blank=True)
    montant   = models.IntegerField(default=0)
    compte    = models.ForeignKey(Compte, on_delete = models.CASCADE, related_name="compte_mouvement")
    employe   = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_payetricycle")
    etat      = models.ForeignKey("coreApp.Etat",  null = True, blank=True, on_delete = models.CASCADE)
    mode      = models.ForeignKey(ModePayement,  null = True, blank=True, on_delete = models.CASCADE, related_name="modepayement_mouvement")
    structure = models.CharField(default=0, max_length = 255, null = True, blank=True)
    numero    = models.CharField(default=0, max_length = 255, null = True, blank=True)
    comment   = models.TextField(default="")



class ReglementApprovisionnement(BaseModel):
    mouvement    = models.ForeignKey(Mouvement, on_delete = models.CASCADE, related_name="mouvement_reglement_appro")
    approvisionnement = models.ForeignKey("approvisionnementApp.Approvisionnement", on_delete = models.CASCADE, related_name="approvisionnement_reglement")
    restait  = models.IntegerField(default=0)


class ReglementCommande(BaseModel):
    mouvement    = models.ForeignKey(Mouvement, on_delete = models.CASCADE, related_name="mouvement_reglement_commande")
    commande  = models.ForeignKey("commandeApp.Commande", on_delete = models.CASCADE, related_name="commande_reglement")
    restait  = models.IntegerField(default=0)

    def __str__(self):
        return self.reglement.reference


class CompteClient(BaseModel):
    mouvement    = models.ForeignKey(Mouvement, on_delete = models.CASCADE, related_name="mouvement_compteclient")
    client  = models.ForeignKey("clientApp.Client", on_delete = models.CASCADE, related_name="client_compte")
    is_dette = models.BooleanField(default=False)

    def __str__(self):
        return self.client.name +" | "+self.mouvement.reference


class ReglementAchatStock(BaseModel):
    mouvement    = models.ForeignKey(Mouvement, on_delete = models.CASCADE, related_name="mouvement_reglement_achatstock")
    achatstock = models.ForeignKey("approvisionnementApp.AchatStock", on_delete = models.CASCADE, related_name="achatstock_reglement")
    restait  = models.IntegerField(default=0)

class ReglementTricycle(BaseModel):
    mouvement    = models.ForeignKey(Mouvement, on_delete = models.CASCADE, related_name="mouvement_reglement")
    tricycle = models.ForeignKey("livraisonApp.Tricycle", on_delete = models.CASCADE, related_name="tricycle_reglement")
    restait  = models.IntegerField(default=0)


class Operation(BaseModel):
    category         = models.ForeignKey(CategoryOperation,  null = True, blank=True, on_delete = models.CASCADE, related_name="category_operation")
    mouvement        = models.ForeignKey(Mouvement,  null = True, blank=True, on_delete = models.CASCADE, related_name="mouvement_operation")
    etat             = models.ForeignKey("coreApp.Etat",  null = True, blank=True, on_delete = models.CASCADE)
    date_approbation = models.DateTimeField(null = True, blank=True)
    image            = models.ImageField(null = True, blank=True)

    def __str__(self):
        return self.category.name +" | "+self.mouvement.reference

class Transfertfond(BaseModel):
    reference          = models.CharField(max_length = 255)
    montant            = models.IntegerField(default=0)
    compte_source      = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_source_transfert")
    compte_destination = models.ForeignKey(Compte,  null = True, blank=True, on_delete = models.CASCADE, related_name="compte_destination_transfert")
    etat               = models.ForeignKey("coreApp.Etat",  null = True, blank=True, on_delete = models.CASCADE)
    employe            = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_transfertfond")
    comment            = models.TextField(default="")





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
        if instance.mouvement.mode.etiquette == ModePayement.PRELEVEMENT:
            CompteClient.objects.create(
                client = instance.commande.groupecommande.client,
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





