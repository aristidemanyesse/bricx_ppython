
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views, fiches

app_name = "fiches"
urlpatterns = [

    
    path('prixparzone/<uuid:id>/', fiches.prixparzone, name="prixparzone"),
    path('commande/<uuid:id>/', fiches.commande, name="commande"),
    path('livraison/<uuid:id>/', fiches.livraison, name="livraison"),
    path('tricycle/<uuid:id>/', fiches.tricycle, name="tricycle"),
    path('approvisionnement/<uuid:id>/', fiches.approvisionnement, name="approvisionnement"),
    path('achatstock/<uuid:id>/', fiches.achatstock, name="achatstock"),
    path('conversion/<uuid:id>/', fiches.conversion, name="conversion"),
    path('production/<uuid:id>/', fiches.production, name="production"),
    path('boncaisse/<uuid:id>/', fiches.boncaisse, name="boncaisse"),
]

