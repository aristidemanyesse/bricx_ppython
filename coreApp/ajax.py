from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
import json, uuid
from django.urls import reverse
import coreApp.tools as tools

from clientApp.forms import *
from approvisionnementApp.forms import *
from commandeApp.forms import *
from livraisonApp.forms import *
from organisationApp.forms import *
from productionApp.forms import *
from comptabilityApp.forms import *
from paramApp.forms import *


# Create your views here.
def save(request):
    if request.method == "POST":
        datas = request.POST
        datas._mutable = True
        for key in datas:
            if datas[key] == "on": datas[key]=True

        try:
            modelform = datas["modelform"]
            MyForm = globals()[modelform]

            if (MyForm) :
                MyModel = tools.form_to_model(modelform)
                content_type = ContentType.objects.get(model= MyModel.lower())
                MyModel = content_type.model_class()

                if "id" in datas and datas["id"] != "":
                    obj = MyModel.objects.get(pk=datas["id"])
                    form = MyForm(datas, request.FILES, instance = obj)
                else:
                    datas["id"] = uuid.uuid4()
                    form = MyForm(datas, request.FILES)

                if form.is_valid():
                    if 'image' in request.FILES and request.FILES["image"] != "":
                        image = request.FILES.get('image')
                        form.image = image

                    item = form.save()
                    if modelform == "ClientForm":
                        return JsonResponse({"status":True, "url" : reverse("boutique:clients:client", args=[item.id])})
                    if modelform == "FournisseurForm":
                        return JsonResponse({"status":True, "url" : reverse("fabrique:appros:fournisseur", args=[item.id])})
                    return JsonResponse({"status":True, "message":"Opération effectuée avec succes !"})
                
                else:
                    errors = form.errors.get_json_data()
                    errors_values = list((list(errors.values())[0][0]).values())
                    errors_keys = list(errors.keys())
                    return JsonResponse({"status":False, "message":"{} : {}".format(errors_keys[0], errors_values[0])})
   
        except Exception as e:
            print("erreur save :", e)
            return JsonResponse({"status":False, "message":"Erreur lors du processus. Veuillez recommencer : "+str(e)})




def mise_a_jour(request):
    if request.method == "POST":
        datas = request.POST
        datas._mutable = True
        for key in datas:
            if datas[key] == "on": datas[key]=True

        try:
            if (datas["model"]) != "":
                modelform = datas["model"]
                content_type = ContentType.objects.get(model= modelform.lower())
                MyModel = content_type.model_class()

                item = MyModel.objects.get(pk=datas["id"])

                mydict = item.__dict__
                del mydict["_state"]
                del mydict["id"]
                mydict[datas["name"]] = datas["val"]
                MyModel.objects.filter(pk=datas["id"]).update(**mydict)

                return JsonResponse({"status": True})

        except Exception as e:
            print("--------------------", e)
            return JsonResponse({"status": False, "message": "Une erreur s'est produite lors de l'opération, veuillez recommencer !"})




def supprimer(request):
    if request.method == "POST":
        datas = request.POST

        try:
            modelform = datas["model"]
            content_type = ContentType.objects.get(model= modelform.lower())
            MyModel = content_type.model_class()

            if "password" in datas and not request.user.check_password(datas["password"]):
                return JsonResponse({"status":False, "message":"Le mot de passe est incorrect !"})

            obj = MyModel.objects.get(pk=datas["id"])
            if obj.protected:
                return JsonResponse({"status":False, "message":"Vous ne pouvez pas supprimer cet element, il est protégé !"})

            if hasattr(obj, "etat"):
                obj.etat = Etat.objects.get(etiquette = Etat.ANNULE)
            else:
                obj.deleted = True
            obj.save()
            return JsonResponse({"status":True, "message":"Suppression effectuée avec succes !"})

        except Exception as e:
            print("erreur save :", e)
            return JsonResponse({"status":False, "message":"Erreur lors du processus. Veuillez recommencer : "+str(e)})




def session(request):
    if request.method == "POST":
        datas = request.POST
        request.session[datas["name"]] = datas["value"]
        return JsonResponse(dict(request.session))



def delete_session(request):
    if request.method == "POST":
        datas = request.POST
        if datas["name"] in request.session:
            del request.session[datas["name"]]
        return JsonResponse(dict(request.session))