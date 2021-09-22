from django.shortcuts import render
from organisationApp.models import Employe
from django.contrib.auth import authenticate
# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request, "auth/pages/login.html")
        

def session(request):
    if request.method == "GET":
        return render(request, "auth/pages/session.html")



def forgetpassword(request):
    return render(request, "auth/pages/forgetpassword.html")



def logout(request):
    return render(request, "auth/pages/forgetpassword.html")
