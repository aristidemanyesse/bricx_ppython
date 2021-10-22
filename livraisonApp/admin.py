from django.contrib import admin
from .models import ModeLivraison, Livraison, Chauffeur, Tricycle, Vehicule, LigneLivraison
# Register your models here.


admin.site.register(ModeLivraison)
admin.site.register(Chauffeur)
admin.site.register(Tricycle)
admin.site.register(Vehicule)
admin.site.register(Livraison)
admin.site.register(LigneLivraison)
