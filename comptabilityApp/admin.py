from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Compte)
admin.site.register(CompteClient)
admin.site.register(Operation)
admin.site.register(CategoryOperation)
admin.site.register(TypeMouvement)
admin.site.register(TypeOperationCaisse)
admin.site.register(Mouvement)
admin.site.register(ModePayement)
admin.site.register(ReglementCommande)
admin.site.register(ReglementTricycle)
admin.site.register(ReglementAchatStock)
admin.site.register(ReglementApprovisionnement)