from django.forms import ModelForm
from .models import Mouvement, TypeMouvement

# Create the form class.
class MouvementForm(ModelForm):
    class Meta:
        model = Mouvement
        fields = "__all__"