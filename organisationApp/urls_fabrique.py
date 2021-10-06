
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views 
from . import traitement 

app_name = "fabrique"
urlpatterns = [
    path('', views.fabrique, name="home"),  

]
