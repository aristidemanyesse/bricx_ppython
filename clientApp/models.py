from django.db import models
from organisationApp.models import Agence, Employe
from coreApp.models import BaseModel, Etat
# Create your models here.



class TypeClient(BaseModel):
    name           = models.CharField(max_length = 255)



class Client(BaseModel):
    name        = models.CharField(max_length = 255, null = False, blank=False)
    adresse         = models.CharField(max_length = 255, null = True, blank=True)
    email            = models.EmailField(max_length = 255, null = True, blank=True)
    contact         = models.CharField(max_length = 255, null = True, blank=True)
    acompte_initial = models.IntegerField(default=0, null = True, blank=True)
    dette_initial   = models.IntegerField(default=0, null = True, blank=True)
    seuil_credit    = models.IntegerField(default=0, null = True, blank=True)
    agence          = models.ForeignKey(Agence, on_delete = models.CASCADE, related_name="client_agence")
    type            = models.ForeignKey(TypeClient, on_delete = models.CASCADE, related_name="type_client")



