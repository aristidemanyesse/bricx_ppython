from django.shortcuts import redirect, render
from organisationApp.models import Employe
from django.contrib.auth import authenticate, logout
# Create your views here.


def login(request):
    if request.method == "GET":
        logout(request)
        if 'locked' in request.session:
            del request.session['locked']
        return render(request, "auth/pages/login.html")
        

def locked(request):
    if request.method == "GET":
        request.session['locked'] = True
        if "last_url" not in request.session:
            request.session['last_url'] = request.META["HTTP_REFERER"]
        return render(request, "auth/pages/locked.html")



def forgetpassword(request):
    return render(request, "auth/pages/forgetpassword.html")


def reset(request):
    return render(request, "auth/pages/reset.html")


def disconnect(request):
    logout(request)
    return redirect("auth:login")




###################################################################################################

def handler404(request, exception):
    return render(request, 'acces/pages/404.html')


def handler400(request, exception):
    return render(request, 'acces/pages/400.html')


def handler500(request):
    return render(request, 'acces/pages/500.html')