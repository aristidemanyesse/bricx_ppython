from .models import  Fournisseur
from django.forms import ModelForm

# Create your models here.




class FournisseurForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Fournisseur

