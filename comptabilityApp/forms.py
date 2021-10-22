from django.forms import ModelForm
from .models import Mouvement, ReglementCommande, TypeMouvement

# Create the form class.
class MouvementForm(ModelForm):
    class Meta:
        model = Mouvement
        fields = "__all__"


class ReglementCommandeForm(ModelForm):
    class Meta:
        model = ReglementCommande
        fields = "__all__"