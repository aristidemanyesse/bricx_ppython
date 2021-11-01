from .models import *
from django.forms import ModelForm
from django.db import models

# Create your models here.


class ChauffeurForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Chauffeur


class VehiculeForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Vehicule


class LivraisonForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Livraison


class LigneLivraisonForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = LigneLivraison


class TricycleForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Tricycle
