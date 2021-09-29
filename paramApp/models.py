from django.db import models
from django.contrib.gis.db import models
# Create your models here.


class MyCompte(models.Model):
    identifiant = models.CharField(max_length = 255)
    expired     = models.DateTimeField(auto_now_add = True)
    tentative   = models.IntegerField(default=3)



class Params(models.Model):
    socialreason          = models.CharField(max_length = 255)
    email                 = models.CharField(max_length = 255)
    contact               = models.CharField(max_length = 255)
    fax                   = models.CharField(max_length = 255)
    postale               = models.CharField(max_length = 255)
    devise                = models.CharField(max_length = 255)
    logo          = models.ImageField(max_length = 255)

    allow_waiting_payment = models.BooleanField(default=True)
    tva                   = models.BooleanField(default=True)

    seuil_credit          = models.BooleanField(default=True)
    production_auto       = models.BooleanField(default=True)
    rupture_stock         = models.BooleanField(default=True)
