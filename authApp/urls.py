
from django.urls import path
from . import views 
from . import ajax 

urlpatterns = [
    path('', views.login),
    path('login/', views.login, name="login"),
    path('locked/', views.locked, name="locked"),
    path('disconnect/', views.disconnect, name="disconnect"),
    path('forgetpassword/', views.forgetpassword, name="forgetpassword"),


    path('ajax/login/', ajax.connexion),
    path('ajax/first_user/', ajax.first_user),

]
