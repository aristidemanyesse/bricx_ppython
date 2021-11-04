
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include

import ficheApp

from . import views 
from . import traitement 

app_name = "fabrique"
urlpatterns = [
    path('', views.dashboard_fabrique, name="dashboard_fabrique"),  
    path('appros/', include("approvisionnementApp.urls") ),
    path('appros/', include("approvisionnementApp.urls") ),
    
    path('production/', include('productionApp.urls')),

    path('rapport_du_jour/<int:year>/<int:month>/<int:day>/', ficheApp.views.rapport_du_jour, name="rapport_du_jour"),
]
