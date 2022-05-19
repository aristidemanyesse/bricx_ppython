from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Production)
admin.site.register(LigneProduction)
admin.site.register(LigneConsommation)
admin.site.register(TypePerte)
admin.site.register(PerteBrique)
admin.site.register(PerteRessource)
admin.site.register(Brique)
admin.site.register(Ressource)
admin.site.register(InitialRessourceAgence)
admin.site.register(InitialBriqueAgence)
admin.site.register(ExigenceProduction)
admin.site.register(LigneExigenceProduction)
