
from django.shortcuts import redirect
from django.urls import path

from . import views
from . import ajax

app_name = "clients"
urlpatterns = [
    path('', views.clients, name="clients"),
    path('<uuid:client_id>/', views.client, name="client"),


    path('ajax/crediter/', ajax.crediter),
    path('ajax/rembourser/', ajax.rembourser),
    path('ajax/regler_toutes_dettes/', ajax.regler_toutes_dettes),
]
