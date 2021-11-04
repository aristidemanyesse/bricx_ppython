
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include
import ficheApp.views

from . import views 


app_name = "boutique"
urlpatterns = [
    path('', views.dashboard_boutique, name="dashboard_boutique"),  

    path('clients/', include("clientApp.urls") ),
    path('commandes/', include("commandeApp.urls") ),
    path('livraisons/', include("livraisonApp.urls") ),

]
