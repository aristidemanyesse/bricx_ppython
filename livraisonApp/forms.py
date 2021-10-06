from .models import Chauffeur, Vehicule, ZoneLivraison, Livraison, LigneLivraison, PrixZoneLivraison, Tricycle
from django.forms import modelForm
from django.db import models

# Create your models here.


class ChauffeurForm(modelForm):
    class Meta:
        model = Chauffeur


class VehiculeForm(modelForm):
    class Meta:
        model = Vehicule



class ZoneLivraisonForm(modelForm):
    class Meta:
        model = ZoneLivraison



class LivraisonForm(modelForm):
    class Meta:
        model = Livraison


class LigneLivraisonForm(modelForm):
    class Meta:
        model = LigneLivraison


class PrixZoneLivraisonForm(modelForm):
    class Meta:
        model = PrixZoneLivraison



class TricycleForm(modelForm):
    class Meta:
        model = Tricycle
