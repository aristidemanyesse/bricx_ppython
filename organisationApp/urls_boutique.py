
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views 


app_name = "boutique"
urlpatterns = [
    path('', views.boutique, name="home"),  

    path('clients/', include("clientApp.urls") ),

    path('commandes/', include("commandeApp.urls") ),
    
    path('livraisons/', include("livraisonApp.urls") ),

]
