from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
import json, uuid
from django.urls import reverse
import coreApp.tools as tools

from clientApp.forms import *
from commandeApp.forms import *


# Create your views here.
def save(request):
    if request.method == "POST":
        modelform = request.POST["modelform"]
        MyForm = globals()[modelform]
        if request.POST["id"] == "":
            request.POST._mutable = True
            request.POST["id"] = uuid.uuid4()

        if (MyForm) :
            MyModel = tools.form_to_model(modelform)
            content_type = ContentType.objects.get(model= MyModel.lower())
            MyModel = content_type.model_class()

            try:
               obj = MyModel.objects.get(pk=request.POST["id"])
               form = MyForm(request.POST, instance = obj)
            except Exception as e:
                form = MyForm(request.POST)

            if form.is_valid():
                item = form.save()
                return JsonResponse({"status":True, "url" : reverse("boutique:clients:client", args=(item.id,))})
            
            else:
                errors = form.errors.get_json_data()
                errors_values = list((list(errors.values())[0][0]).values())
                errors_keys = list(errors.keys())
                return JsonResponse({"status":False, "message":"{} : {}".format(errors_keys[0], errors_values[0])})
   
        else:
            return JsonResponse({"status":False, "message":"Erreur lors du processus. Veuillez recommencer !"})
