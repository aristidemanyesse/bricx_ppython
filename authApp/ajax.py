from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render
from authApp.models import ForgotPassword
from organisationApp.models import Employe
from django.contrib.auth import authenticate, login
from django.http import  JsonResponse
import uuid, datetime
from django.contrib.sessions.backends.db import SessionStore
# Create your views here.

def connexion(request):
    if request.method == "POST":
        datas = request.POST
        user = authenticate(request, username=datas["login"], password=datas["password"])
        if user is not None:
            try:
                profile = Employe.objects.get(id = user.id)
                if profile.is_never_connected:
                    request.session["user_id"] = profile.id
                    return JsonResponse({"status":True, "new":True})
                login(request, user)
                return JsonResponse({"status":True})
            except Exception as e:
                print("-----------------------------------", e)
                return JsonResponse({"status":False, "message":"Une erreur s'est produite lors de l'opération, veuillez recommencer !"})
        else:
            return JsonResponse({"status":False, "message":"Login et/ou mot de passe incorrect !"})



def unlocked(request):
    if request.method == "POST":
        datas = request.POST
        user = authenticate(request, username=datas["username"], password=datas["password"])
        if user is not None:
            try:
                login(request, user)
                url = request.session['last_url']
                if 'locked' in request.session:
                    del request.session['locked']
                    del request.session['last_url']
                return JsonResponse({"status":True, "url":url})
            except Exception as e:
                print("-----------------------------------", e)
                return JsonResponse({"status":False, "message":"Une erreur s'est produite lors de l'opération, veuillez recommencer !"})
        else:
            return JsonResponse({"status":False, "message":"Mot de passe incorrect !"})




def first_user(request):
    if request.method == "POST":
        datas = request.POST
        if len(datas["password"]) >= 4:
            if datas["password1"] == datas["password"]:
                try:
                    user = Employe.objects.get(id = request.session["user_id"])
                    user.username = datas["login"]
                    user.set_password(datas["password"])
                    user.is_never_connected = False
                    user.save()

                    user = authenticate(request, username=datas["login"], password=datas["password"])
                    login(request, user)
                    res = JsonResponse({"status":True})

                except Exception as e:
                    print("-----------------------------------", e)
                    res = JsonResponse({"status":False, "message": e})
            else:
                res = JsonResponse({"status":False, "message":"Les mots de passe ne correspondent pas !"})
        else:
            res = JsonResponse({"status":False, "message":"Le nouveau mot de passe est trop court, minimum 8 caractères !"})

        return res





def forgetpassword(request):
    if request.method == "POST":
        datas = request.POST
        try :
            user = User.objects.get(email = datas["email"])
            ForgotPassword.objects.create(
                    email = datas["email"]
                )
            return JsonResponse({"status":True, "url":"/auth/reset/"})
        except Exception as e:
            print(e)
            return JsonResponse({"status":False, "message":"Désolé, cette adresse email n'est pas connu par le ssytème !"})




def reset(request):
    if request.method == "POST":
        datas = request.POST
        if datas["password"] == datas["confirm"]:
            try :
                fp = ForgotPassword.objects.get(pk = id, is_validate = False)
                if fp.finished_at >= datetime.datetime.now():
                    user = User.objects.get(email = fp.email)
                    user.set_password(datas["password"])
                    user.save()

                    fp.is_validate = True
                    fp.save()
                    return JsonResponse({"status":True, "url":"/auth/login/"})
                else:
                    return JsonResponse({"status":False, "message":"La période pour changer le mot de passe avec ce mail a expiré, veuillez recommencer la procédure !"})
            except Exception as e:
                print(e)
                return JsonResponse({"status":False, "message":"Une erreur s'est produite lors del'opération, veuillez recommencer !"})
        else:
            return JsonResponse({"status":False, "message":"Les mots de passe ne correspondent pas !"})




def logout(request):
    return render(request, "login.html")