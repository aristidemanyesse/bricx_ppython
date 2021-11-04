
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views, fiches

app_name = "fiches"
urlpatterns = [
    
    path('rapport_du_jour/<int:year>/<int:month>/<int:day>/', views.rapport_du_jour, name="rapport_du_jour"),



    path('prixparzone/<uuid:id>/', fiches.prixparzone, name="prixparzone"),
    path('commande/<uuid:id>/', fiches.commande, name="commande"),
    path('livraison/<uuid:id>/', fiches.livraison, name="livraison"),
    path('approvisionnement/<uuid:id>/', fiches.approvisionnement, name="approvisionnement"),
    path('achatstock/<uuid:id>/', fiches.achatstock, name="achatstock"),
    path('boncaisse/<uuid:id>/', fiches.boncaisse, name="boncaisse"),
]

