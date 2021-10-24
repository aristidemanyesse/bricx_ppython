from .models import PerteBrique, PerteRessource
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

