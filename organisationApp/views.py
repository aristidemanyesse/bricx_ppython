from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from organisationApp.models import Employe
from django.contrib.auth import authenticate
# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request, "pages/login.html")
        

def reconnect(request):
    return render(request, "pages/login.html")



def forgetpassword(request):
    return render(request, "pages/forgetpassword.html")



def logout(request):
    return redirect("auth/", permanent=True)