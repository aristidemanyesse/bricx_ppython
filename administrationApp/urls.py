
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views, ajax

app_name = "administration"
urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    
    path('general/', views.general, name="general"),
    path('roles/', views.roles, name="roles"),
    path('mycompte/', views.mycompte, name="mycompte"),

    
    path('organisation/', views.organisation, name="organisation"),
    path('production/', views.production, name="production"),
    path('prices/', views.prices, name="prices"),
    path('caisse/', views.caisse, name="caisse"),


    path('organisation/ajax/exigence/', ajax.exigence, name="exigence"),
    path('organisation/ajax/price/', ajax.price, name="price"),
    path('organisation/ajax/paye_produit/', ajax.paye_produit, name="paye_produit"),
    path('organisation/ajax/paye_produit_ferie/', ajax.paye_produit_ferie, name="paye_produit_ferie"),
]

