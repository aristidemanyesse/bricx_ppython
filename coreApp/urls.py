
from django.urls import path
from . import ajax

app_name = "core"
urlpatterns = [
    path('ajax/save/', ajax.save, name="save"),
    path('ajax/session/', ajax.session, name="session"),
    path('ajax/delete_session/', ajax.delete_session, name="delete_session"),

]
