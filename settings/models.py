from django.db import models

# Create your models here.

class MyCompte():
    identifiant = models.CharField(max_length = 255)
    expired = models.CharField(max_length = 255)
    tentative = models.IntegerField(max_length = 255)


