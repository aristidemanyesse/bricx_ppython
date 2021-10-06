
from django.urls import path
from . import ajax

app_name = "core"
urlpatterns = [
    path('ajax/save/', ajax.save, name="save"),

]
