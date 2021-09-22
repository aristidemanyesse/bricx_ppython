from django.db import models

# Create your models here.


class MyCompte():
    identifiant = models.CharField(max_length = 255)
    expired     = models.CharField(max_length = 255)
    tentative   = models.IntegerField(max_length = 255)



class Params():
    societe               = models.CharField(max_length = 255)
    email                 = models.CharField(max_length = 255)
    contatct              = models.IntegerField(max_length = 255)
    fax                   = models.IntegerField(max_length = 255)
    postale               = models.IntegerField(max_length = 255)
    devise                = models.IntegerField(max_length = 255)

    allow_waiting_payment = models.BooleanField(default=True)
    tva                   = models.BooleanField(default=True)

    seuil_credit          = models.BooleanField(default=True)
    production_auto       = models.BooleanField(default=True)
    rupture_stock         = models.BooleanField(default=True)

