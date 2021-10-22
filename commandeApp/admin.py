from django.contrib import admin
from .models import Conversion, GroupeCommande, Commande, LigneCommande, LigneConversion, ZoneLivraison, PrixZoneLivraison
# Register your models here.


admin.site.register(GroupeCommande)
admin.site.register(Commande)
admin.site.register(LigneCommande)
admin.site.register(Conversion)
admin.site.register(LigneConversion)
admin.site.register(ZoneLivraison)
admin.site.register(PrixZoneLivraison)
