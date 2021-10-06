from django.db import models
import approvisionnementApp.models as appro_models
import commandeApp.models as commande_models
import livraisonApp.models as livraison_models
import productionApp.models as production_models
import organisationApp.models as organisation_models
import clientApp.models as client_models
import coreApp.models as core_models
import comptabilityApp.models as comptability_models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver




class Agence(core_models.BaseModel):
    name   = models.CharField(max_length = 255)
    lieu   = models.CharField(max_length = 255, null = True, blank=True)


class Employe(User, core_models.BaseModel):
    telephone          = models.CharField(max_length = 255, null = True, blank=True)
    adresse            = models.CharField(max_length = 255, null = True, blank=True)
    is_never_connected = models.BooleanField(default = True)
    is_allowed         = models.BooleanField(default = True)
    agence             = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_employe")
    avatar          = models.ImageField(upload_to = "storage/images/employes/", max_length=255,  null=True, blank=True)

    def __str__(self):
        return self.first_name+" "+self.last_name





######################################################################################################
##### SIGNAUX



@receiver(pre_save, sender = Employe)
def pre_save_employe(sender, instance, **kwargs):
    if instance._state.adding:
        instance.set_password(instance.password)
