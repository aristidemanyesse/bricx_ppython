from django.contrib import admin

from .models import  Fournisseur,Approvisionnement

# Register your models here.

admin.site.register(Approvisionnement)
admin.site.register(Fournisseur)