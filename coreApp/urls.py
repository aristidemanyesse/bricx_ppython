
from django.urls import path
from . import ajax

app_name = "core"
urlpatterns = [
    path('ajax/save/', ajax.save, name="save"),
    path('ajax/mise_a_jour/', ajax.mise_a_jour, name="mise_a_jour"),
    path('ajax/supprimer/', ajax.supprimer, name="supprimer"),
    path('ajax/session/', ajax.session, name="session"),

]
