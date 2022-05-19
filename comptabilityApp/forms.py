from django.forms import ModelForm
from .models import *

# Create the form class.
class MouvementForm(ModelForm):
    class Meta:
        model = Mouvement
        fields = "__all__"


class ReglementCommandeForm(ModelForm):
    class Meta:
        model = ReglementCommande
        fields = "__all__"



class CategoryOperationForm(ModelForm):
    class Meta:
        model = CategoryOperation
        fields = "__all__"


class CompteForm(ModelForm):
    class Meta:
        model = Compte
        fields = "__all__"