
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views

app_name = "fiches"
urlpatterns = [
    path('prixparzone/<uuid:id>/', views.prixparzone, name="prixparzone"),
    path('commande/<uuid:id>/', views.commande, name="commande"),
    path('livraison/<uuid:id>/', views.livraison, name="livraison"),
    path('tricycle/<uuid:id>/', views.tricycle, name="tricycle"),
    path('approvisionnement/<uuid:id>/', views.approvisionnement, name="approvisionnement"),
    path('achatstock/<uuid:id>/', views.achatstock, name="achatstock"),
    path('conversion/<uuid:id>/', views.conversion, name="conversion"),
    path('production/<uuid:id>/', views.production, name="production"),
    path('boncaisse/<uuid:id>/', views.boncaisse, name="boncaisse"),
]

