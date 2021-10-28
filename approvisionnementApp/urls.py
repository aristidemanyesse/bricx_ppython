
from django.shortcuts import redirect
from django.urls import path

from . import views, ajax, ajax_fournisseur

app_name = "appros"
urlpatterns = [
    path('', views.approvisionnements, name="approvisionnements"),
    path('fournisseurs', views.fournisseurs, name="fournisseurs"),
    path('fournisseur/<uuid:fournisseur_id>/', views.fournisseur, name="fournisseur"),


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
]
