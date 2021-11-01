from .models import MyApp, MyCompte
from django.forms import ModelForm

# Create your models here.


class MyAppForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = MyApp



class MyCompteForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = MyCompte

