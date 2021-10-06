from django.contrib import admin
from .models import GroupeCommande, Commande, ZoneLivraison, PrixZoneLivraison
# Register your models here.


admin.site.register(GroupeCommande)
admin.site.register(Commande)
admin.site.register(ZoneLivraison)
admin.site.register(PrixZoneLivraison)
