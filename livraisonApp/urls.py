
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views 
from . import ajax 

app_name = "livraisons"
urlpatterns = [
    path('', views.livraisons, name="livraisons"),  


    path('ajax/livraison/', ajax.livraison, name="livraison"),  
    path('ajax/retour_livraison/', ajax.retour_livraison, name="retour_livraison"),  

]
