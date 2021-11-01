from .models import *
from django.forms import ModelForm
# Create your models here.


class GroupeCommandeForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = GroupeCommande


class CommandeForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Commande


class LigneCommandeForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = LigneCommande



class ZoneLivraisonForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = ZoneLivraison



class PrixZoneLivraisonForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = PrixZoneLivraison
