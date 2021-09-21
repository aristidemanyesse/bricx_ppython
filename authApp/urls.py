
from django.urls import path
from . import views 
from . import traitement 

urlpatterns = [
    path('/', views.login),
    path('login', views.login, name="login"),
    path('traitement/login', traitement.connexion),
    path('traitement/first_user', traitement.first_user),

    path('forgetpassword/', views.forgetpassword, name="forgetpassword"),
]
