from django.db import models
# Create your models here.


class MyCompte(models.Model):
    identifiant = models.CharField(max_length = 255)
    expiration     = models.DateTimeField(default = "")
    tentative   = models.IntegerField(default=3)



class MyApp(models.Model):
    socialreason          = models.CharField(max_length = 255)
    email                 = models.CharField(max_length = 255)
    contact               = models.CharField(max_length = 255, null = True, blank=True)
    adresse               = models.CharField(max_length = 255, null = True, blank=True)
    fax                   = models.CharField(max_length = 255, null = True, blank=True)
    postale               = models.CharField(max_length = 255, null = True, blank=True)
    devise                = models.CharField(max_length = 255, null = True, blank=True)
    logo                  = models.ImageField(upload_to = "storage/images/params/", max_length=255, null=True, blank=True)

    allow_waiting_payment = models.BooleanField(default=True, null = True, blank=True)
    tva                   = models.IntegerField(default=0, null = True, blank=True)
    seuil_credit          = models.IntegerField(default=0, null = True, blank=True)
    production_auto       = models.BooleanField(default=True, null = True, blank=True)

    class Meta:
        permissions = [
            ("fabrique", "BRICX | Peut acceder à la gestion de la fabrique"),
            ("boutique", "BRICX | Peut acceder à la gestion de la boutique"),
            ("production", "BRICX | Peut acceder à la gestion de la production"),
            ("organisation", "BRICX | Peut acceder à la gestion de l'organisation"),
            ("commande", "BRICX | Peut acceder à la gestion des commande"),
            ("livraisons", "BRICX | Peut acceder à la gestion des livraisons"),
            ("approvisionnement", "BRICX | Peut acceder à la gestion des approvisionnement"),
            ("comptabilitte", "BRICX | Peut acceder à la gestion des comptabilitte"),
            ("tresorerie", "BRICX | Peut acceder à la tresorerie"),
            ("administration", "BRICX | Peut acceder aux administrations"),
            ("role", "BRICX | Peut acceder aux accès utilisateurs"),
        ]
