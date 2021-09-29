from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from organisationApp.models import Employe
from django.contrib.auth import authenticate
# Create your views here.


def dashboard(request, id):
    if request.method == "GET":
        return render(request, "organisation/pages/dashboard.html")
