from django.db import models
from coreApp.models import BaseModel
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver




class Agence(BaseModel):
    name   = models.CharField(max_length = 255)
    lieu   = models.CharField(max_length = 255, null = True, blank=True)


class Employe(User, BaseModel):
    telephone          = models.CharField(max_length = 255, null = True, blank=True)
    adresse            = models.CharField(max_length = 255, null = True, blank=True)
    is_never_connected = models.BooleanField(default = True)
    is_allowed         = models.BooleanField(default = True)
    agence             = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_employe")

    def __str__(self):
        return self.first_name+" "+self.last_name





######################################################################################################
##### SIGNAUX



@receiver(pre_save, sender = Employe)
def pre_save_employe(sender, instance, **kwargs):
    if instance._state.adding:
        instance.set_password(instance.password)
