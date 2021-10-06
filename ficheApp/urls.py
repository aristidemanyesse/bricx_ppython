
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

from . import views

app_name = "fiches"
urlpatterns = [
    path('prixparzone/<uuid:id>/', views.prixparzone, name="prixparzone"),
]

