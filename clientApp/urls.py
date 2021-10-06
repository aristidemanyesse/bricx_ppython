
from django.shortcuts import redirect
from django.urls import path

from . import views

app_name = "clients"
urlpatterns = [
    path('', views.clients, name="clients"),
    path('<uuid:client_id>/', views.client, name="client"),
]
