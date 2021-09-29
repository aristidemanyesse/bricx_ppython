
from django.urls import path
from . import views 
from . import traitement 


urlpatterns = [
    path('', views.dashboard, name="agence"),

]
