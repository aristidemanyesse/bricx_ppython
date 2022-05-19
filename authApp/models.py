from django.db import models

from django.db import models, transaction
import uuid, datetime, json, random
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from coreApp.models import BaseModel


class ForgotPassword(BaseModel):
    email       = models.EmailField(null = False, blank = False)
    finished_at = models.DateTimeField(default = "")
    is_validate = models.BooleanField(default = False)

    def __str__(self):
        return self.email



class AccesAgence(BaseModel):
    agence = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_acces")
    employe = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_acces")

    def __str__(self):
        return self.employe.first_name + " " + self.employe.last_name + " dans " + self.agence.name

    
    def name(self):
        return self.employe.first_name + " " + self.employe.last_name + " dans " + self.agence.name


######################################################################################################
##### SIGNAUX



@receiver(pre_save, sender = ForgotPassword)
def pre_save_forgetpassword(sender, instance, **kwargs):
    if instance._state.adding:
        instance.finished_at = datetime.datetime.now(x) + datetime.timedelta(hours=4)



@receiver(post_save, sender = ForgotPassword)
def post_save_forgetpassword(sender, instance, **kwargs):
    pass
    #TODO: faire un envoi de mail