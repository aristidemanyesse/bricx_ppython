from .models import TypeClient, Client
from django.forms import ModelForm

# Create your models here.


class TypeClientForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = TypeClient



class ClientForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Client

