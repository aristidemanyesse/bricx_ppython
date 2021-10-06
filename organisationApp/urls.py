
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views 
from . import traitement 

app_name = "organisation"
urlpatterns = [
    path('', views.home, name="home"),  

]
