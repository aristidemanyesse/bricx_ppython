from django.db import models
from coreApp.models import BaseModel
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver




class Agence(BaseModel):
    name   = models.CharField(max_length = 255)
    lieu   = models.CharField(max_length = 255, null = True, blank=True)
    compte = models.ForeignKey("Compte", on_delete = models.CASCADE, related_name="agence_compte")


class Employe(User, BaseModel):
    telephone          = models.CharField(max_length = 255, null = True, blank=True)
    adresse            = models.CharField(max_length = 255, null = True, blank=True)
    is_never_connected = models.BooleanField(default = True)
    is_allowed         = models.BooleanField(default = True)
    agence             = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")

    def __str__(self):
        return self.first_name+" "+self.last_name


class AccesAgence(BaseModel):
    agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    employe = models.ForeignKey(Employe, on_delete = models.CASCADE, related_name="employe_acces")


class Role(BaseModel):
    name   = models.CharField(max_length = 255)

class RoleEmploye(BaseModel):
    role = models.ForeignKey(Role, on_delete = models.CASCADE, related_name="role_acces")
    employe = models.ForeignKey(Employe, on_delete = models.CASCADE, related_name="employe_role")



class ForgotPassword(BaseModel):
    email       = models.EmailField(null = False, blank = False)
    finished_at = models.DateTimeField(default = "")
    is_validate = models.BooleanField(default = False)
    employe     = models.ForeignKey(Employe, on_delete = models.CASCADE, blank = True, null = True, related_name="employe_forgotpassword")

    def __str__(self):
        return self.email




######################################################################################################
##### SIGNAUX



@receiver(pre_save, sender = Employe)
def pre_save_employe(sender, instance, **kwargs):
    if instance._state.adding:
        instance.set_password(instance.password)
