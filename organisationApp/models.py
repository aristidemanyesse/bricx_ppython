from authApp.models import Utilisateur
from comptabilityApp.models import Compte
from django.db import models
from coreApp.models import BaseModel, MyCodeException
from django.contrib.auth.models import User
import uuid, datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver



class Agence(BaseModel):
    name   = models.CharField(max_length = 255)
    lieu   = models.CharField(max_length = 255, null = True, blank=True)
    compte = models.ForeignKey(Compte, on_delete = models.CASCADE, related_name="agence_compte")




class AccesAgence(BaseModel):
    agence = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="agence_acces")
    utilisateur = models.ForeignKey(Utilisateur, on_delete = models.CASCADE, related_name="utilisateur_acces")


