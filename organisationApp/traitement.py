from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render
from organisationApp.models import Employe
from django.contrib.auth import authenticate, login
from django.http import  JsonResponse
# import webapp2
# from webapp2_extras import sessions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


def connexion(request):
    if request.method == "POST":
        datas = request.POST
        user = authenticate(request, username=datas["login"], password=datas["password"])
        if user is not None:
            try:
                profile = Employe.objects.get(id = user.id)
                if profile.is_never_connected:
                    return JsonResponse({"status":True, "new":True})
                return JsonResponse({"status":True})
            except Exception as e:
                print("-----------------------------------", e)
                return JsonResponse({"status":False, "message": _("Une erreur s'est produite lors de l'opération, veuillez recommencer !")})
        else:
            return JsonResponse({"status":False, "message": _("Login et/ou mot de passe incorrect !")})



def first_user(request):
    datas = request.POST
    if len(datas["password"]) >= 8:
        if datas["password1"] == datas["password"]:
            try:
                user = Employe.objects.get(id = "")
                user.username = datas["login"]
                user.set_password(datas["password"])
                user.is_nerver_connected = False
                user.save()
                login(request, user)
                res = JsonResponse({"status":True, })

            except Exception as e:
                print("-----------------------------------", e)
                res = JsonResponse({"status":False, "message": e})
        else:
            res = JsonResponse({"status":False, "message": _("Les mots de passe ne correspondent pas !")})
    else:
        res = JsonResponse({"status":False, "message": _("Le nouveau mot de passe est trop court, minimum 8 caractères !")})

    return res





def forgetpassword(request):
    return render(request, "pages/forgetpassword.html")




def logout(request):
    return render(request, "login.html")