
from django.urls import path
from . import views 
from . import traitement 


urlpatterns = [
    path('', views.login),
    path('login/', views.login, name="login"),
    path('forgetpassword/', views.forgetpassword, name="forgetpassword"),
    path('session/', views.session, name="session"),
    path('logout/', views.logout, name="logout"),

    path('traitement/login/', traitement.connexion),
    path('traitement/first_user/', traitement.first_user),

]
