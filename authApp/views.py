from django.shortcuts import redirect, render
from organisationApp.models import Employe
from django.contrib.auth import authenticate, logout
# Create your views here.


def login(request):
    if request.method == "GET":
        logout(request)
        return render(request, "auth/pages/login.html")
        

def locked(request):
    if request.method == "GET":
        return render(request, "auth/pages/locked.html")



def forgetpassword(request):
    return render(request, "auth/pages/forgetpassword.html")



def disconnect(request):
    logout(request)
    return redirect("/auth/")
