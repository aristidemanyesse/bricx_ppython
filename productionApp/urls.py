
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views
from . import ajax

app_name = "production"
urlpatterns = [
    path('productions', views.productions, name="productions"),  
    path('stock_brique', views.stock_brique, name="stock_brique"),  
    path('stock_ressource', views.stock_ressource, name="stock_ressource"),  
    path('perte_ressource', views.perte_ressource, name="perte_ressource"),  
    path('perte_brique', views.perte_brique, name="perte_brique"),  

    path('rapport_production/', views.rapport_production, name="rapport_production"),


    path('ajax/calcul_production/', ajax.calcul_production, name="calcul_production"), 
    path('ajax/new_production/', ajax.new_production, name="new_production"), 
    path('ajax/rangement/', ajax.rangement, name="rangement"), 
  ]
