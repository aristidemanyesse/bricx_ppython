
from django.shortcuts import redirect
from django.urls import path

from . import views, ajax, ajax_fournisseur, ajax_achatstock

app_name = "appros"
urlpatterns = [
    path('', views.approvisionnements, name="approvisionnements"),
    path('fournisseurs', views.fournisseurs, name="fournisseurs"),
    path('fournisseur/<uuid:fournisseur_id>/', views.fournisseur, name="fournisseur"),
    path('achatstock', views.achatstock, name="achatstock"),


    path('ajax/crediter/', ajax_fournisseur.crediter),
    path('ajax/rembourser/', ajax_fournisseur.rembourser),
    path('ajax/regler_toutes_dettes/', ajax_fournisseur.regler_toutes_dettes),


    path('ajax/new_ressource/', ajax.new_ressource),
    path('ajax/delete_ligne/', ajax.delete_ligne),
    path('ajax/actualise/', ajax.actualise),
    path('ajax/total/', ajax.total),
    path('ajax/valider_approvisionnement/', ajax.valider_approvisionnement),
    path('ajax/terminer_appro/', ajax.terminer_appro),
    path('ajax/regler_appro/', ajax.regler_appro),

    path('ajax_achatstock/new_produit/', ajax_achatstock.new_produit),
    path('ajax_achatstock/delete_ligne/', ajax_achatstock.delete_ligne),
    path('ajax_achatstock/actualise/', ajax_achatstock.actualise),
    path('ajax_achatstock/total/', ajax_achatstock.total),
    path('ajax_achatstock/valider_achatstock/', ajax_achatstock.valider_achatstock),
    path('ajax_achatstock/terminer_achat/', ajax_achatstock.terminer_achat),
    path('ajax_achatstock/regler_achat/', ajax_achatstock.regler_achat),
]
