
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views

app_name = "commandes"
urlpatterns = [
    path('', views.commandes, name="commandes"),  
    path('commandes1', views.commandes1, name="commandes1"),  
    path('prixparzone', views.prixparzone, name="prixparzone"), 
]
