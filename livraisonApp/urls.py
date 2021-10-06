
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views 

app_name = "livraison"
urlpatterns = [
    path('', views.livraisons, name="livraisons"),  
    

]
