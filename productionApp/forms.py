from .models import *
from django.forms import ModelForm

# Create your models here.


class PerteBriqueForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = PerteBrique



class PerteRessourceForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = PerteRessource



class BriqueForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Brique




class RessourceForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Ressource

