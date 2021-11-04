
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

import ficheApp.views, comptabilityApp.views

from . import views 

app_name = "manager"
urlpatterns = [
    path('', views.dashboard_manager, name="dashboard_manager"),  
    path('caisse/', comptabilityApp.views.caisse, name="caisse"),  
    path('appros/', include("approvisionnementApp.urls") ),
    path('appros/', include("approvisionnementApp.urls") ),

    path('production/', include('productionApp.urls')),

    path('rapport_du_jour/<int:year>/<int:month>/<int:day>/', ficheApp.views.rapport_du_jour, name="rapport_du_jour"),
]
