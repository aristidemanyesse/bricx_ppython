from django.contrib import admin
from .models import LigneConsommation, Brique, LigneProduction, Production, Ressource
# Register your models here.


admin.site.register(Production)
admin.site.register(LigneProduction)
admin.site.register(LigneConsommation)
admin.site.register(Brique)
admin.site.register(Ressource)
