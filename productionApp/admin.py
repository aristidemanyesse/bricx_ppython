from django.contrib import admin
from .models import LigneConsommation, Brique, LigneProduction, Production, Ressource, TypePerte, PerteBrique, PerteRessource
# Register your models here.


admin.site.register(Production)
admin.site.register(LigneProduction)
admin.site.register(LigneConsommation)
admin.site.register(TypePerte)
admin.site.register(PerteBrique)
admin.site.register(PerteRessource)
admin.site.register(Brique)
admin.site.register(Ressource)
