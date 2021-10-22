
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views 
from . import ajax 

app_name = "livraison"
urlpatterns = [
    path('', views.livraisons, name="livraisons"),  


    path('ajax/livraison/', ajax.livraison, name="livraison"),  

]
