from .models import GroupeCommande, Commande, LigneCommande
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

