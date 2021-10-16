from django.contrib import admin
from .models import TypeOperationCaisse, Operation, CategoryOperation, Compte, CompteClient, ReglementCommande, TypeReglement, Mouvement, TypeMouvement, ModePayement
# Register your models here.
admin.site.register(Compte)
admin.site.register(CompteClient)
admin.site.register(Operation)
admin.site.register(CategoryOperation)
admin.site.register(TypeMouvement)
admin.site.register(TypeOperationCaisse)
admin.site.register(Mouvement)
admin.site.register(ModePayement)
admin.site.register(TypeReglement)
admin.site.register(ReglementCommande)