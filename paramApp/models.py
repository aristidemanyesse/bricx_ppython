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
    image                  = models.ImageField(upload_to = "stockage/images/params/", max_length=255, null=True, blank=True)

    allow_waiting_payment = models.BooleanField(default=True, null = True, blank=True)
    tva                   = models.IntegerField(default=0, null = True, blank=True)
    seuil_credit          = models.IntegerField(default=0, null = True, blank=True)
    production_auto       = models.BooleanField(default=True, null = True, blank=True)

    class Meta:
        permissions = [
            ("fabrique", "~ Acccès à la gestion de la fabrique"),
            ("boutique", "~ Acccès à la gestion de la boutique"),
            ("production", "~ Acccès à la gestion de la production"),
            ("organisation", "~ Acccès à la gestion de l'organisation"),
            ("commande", "~ Acccès à la gestion des commande"),
            ("livraison", "~ Acccès à la gestion des livraisons"),
            ("stock", "~ Acccès à la gestion des stock"),
            ("approvisionnement", "~ Acccès à la gestion des approvisionnements"),
            ("comptabilite", "~ Acccès à la gestion des comptabilité"),
            ("tresorerie", "~ Acccès à la tresorerie"),
            ("administration", "~ Acccès aux administrations"),
            ("manager", "~ Acccès à la gestion globale"),
            ("role", "~ Acccès aux accès utilisateurs"),
            ("CREATE", "~ Peut enregistrer des informations"),
            ("UPDATE", "~ Peut modifier des informations"),
            ("DELETE", "~ Peut supprimer des informations"),
        ]
