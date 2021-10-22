
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views
from . import ajax_new_commande

app_name = "commandes"
urlpatterns = [
    path('', views.commandes, name="commandes"),  
    path('commandes1/', views.commandes1, name="commandes1"),  
    path('prixparzone/', views.prixparzone, name="prixparzone"), 
    path('conversions/', views.conversions, name="conversions"),  


    path('ajax_new_commande/new_produit/', ajax_new_commande.new_produit, name="new_produit"), 
    path('ajax_new_commande/delete_ligne/', ajax_new_commande.delete_ligne, name="delete_ligne"), 
    path('ajax_new_commande/actualise/', ajax_new_commande.actualise, name="actualise"), 
    path('ajax_new_commande/total/', ajax_new_commande.total, name="total"), 
    path('ajax_new_commande/valider_commande/', ajax_new_commande.valider_commande, name="valider_commande"), 
    path('ajax_new_commande/changer_produit/', ajax_new_commande.changer_produit, name="changer_produit"), 
    path('ajax_new_commande/regler_commande/', ajax_new_commande.regler_commande, name="regler_commande"), 
]
