from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from comptabilityApp.models import Compte

from coreApp.models import BaseModel
import productionApp.models 


class Agence(BaseModel):
    name   = models.CharField(max_length = 255)
    lieu   = models.CharField(max_length = 255, null = True, blank=True)


class Employe(User, BaseModel):
    telephone          = models.CharField(max_length = 255, null = True, blank=True)
    adresse            = models.CharField(max_length = 255, null = True, blank=True)
    is_never_connected = models.BooleanField(default = True)
    is_allowed         = models.BooleanField(default = True)
    agence             = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_employe")
    avatar          = models.ImageField(upload_to = "storage/images/employes/", max_length=255,  null=True, blank=True)

    def __str__(self):
        return self.first_name+" "+self.last_name

    def name(self):
        return self.first_name+" "+self.last_name



######################################################################################################
##### SIGNAUX


@receiver(post_save, sender = Agence)
def post_save_agence(sender, instance, created, **kwargs):
    if created:
        Compte.objects.create(
            name = "Compte de "+instance.name,
            agence = instance,
            initial_amount = 0
        )

        for item in productionApp.models.Brique.objects.filter(deleted = False):
            productionApp.models.InitialBriqueAgence.objects.create(
                brique = item,
                agence = instance,
                quantite = 0
            )

        for item in productionApp.models.Ressource.objects.filter(deleted = False):
            productionApp.models.InitialRessourceAgence.objects.create(
                ressource = item,
                agence = instance,
                quantite = 0
            )




@receiver(pre_save, sender = Employe)
def pre_save_employe(sender, instance, **kwargs):
    if instance._state.adding:
        instance.set_password(instance.password)
