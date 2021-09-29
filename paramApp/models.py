from django.db import models
from django.contrib.gis.db import models
# Create your models here.


class MyCompte(models.Model):
    identifiant = models.CharField(max_length = 255)
    expiration     = models.DateTimeField(default = "")
    tentative   = models.IntegerField(default=3)



class MyApp(models.Model):
    socialreason          = models.CharField(max_length = 255)
    email                 = models.CharField(max_length = 255)
    contact               = models.CharField(max_length = 255)
    fax                   = models.CharField(max_length = 255)
    postale               = models.CharField(max_length = 255)
    devise                = models.CharField(max_length = 255)
    logo          = models.ImageField(upload_to = "storage/images/params/", max_length=255)

    allow_waiting_payment = models.BooleanField(default=True)
    tva                   = models.BooleanField(default=True)

    seuil_credit          = models.BooleanField(default=True)
    production_auto       = models.BooleanField(default=True)
    rupture_stock         = models.BooleanField(default=True)

    class Meta:
        permissions = [
            ("fabrique", "Peut acceder à la gestion de la fabrique"),
            ("boutique", "Peut acceder à la gestion de la boutique"),
            ("production", "Peut acceder à la gestion de la production"),
            ("organisation", "Peut acceder à la gestion de l'organisation"),
            ("commande", "Peut acceder à la gestion des commande"),
            ("approvisionnement", "Peut acceder à la gestion des approvisionnement"),
            ("comptabilitte", "Peut acceder à la gestion des comptabilitte"),
            ("configuration", "Peut acceder aux configurations"),
            ("role", "Peut acceder aux accès utilisateurs"),
        ]
