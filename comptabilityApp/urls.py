
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views, ajax

app_name = "tresorerie"
urlpatterns = [
    path('caisse', views.caisse, name="caisse"),  


    path('ajax/operation/', ajax.operation, name="operation"), 
    path('ajax/transfert/', ajax.transfert, name="transfert"), 
    path('ajax/valider_mouvement/', ajax.valider_mouvement, name="valider_mouvement"), 
  ]
