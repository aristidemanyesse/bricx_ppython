from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from commandeApp.models import PrixZoneLivraison
import coreApp.tools as tools
from productionApp.models import ExigenceProduction, LigneExigenceProduction, PayeBrique, PayeBriqueFerie


def exigence(request):
    if request.method == "POST":
        datas = request.POST
        try:
            exigence = ExigenceProduction.objects.get(pk=datas["id"])
            exigence.quantite = datas["quantite"]
            exigence.save()

            for key in datas:
                try:
                    LigneExigenceProduction.objects.filter(pk=key).update(quantite = datas[key])
                except :
                    pass
            
            return JsonResponse({"status": True})

        except Exception as e:
            print("--------------------", e)
            return JsonResponse({"status": False, "message":"Une erreur s'est produite lors de l'opération, veuillez recommencer !"})
        


def price(request):
    if request.method == "POST":
        datas = request.POST
        try:
            for item in datas["tableau"].split(","):
                if "=" in item:
                    id, price = item.split("=")
                    PrixZoneLivraison.objects.filter(id=id).update(price = price)
                    
            return JsonResponse({"status": True})

        except Exception as e:
            print("--------------------", e)
            return JsonResponse({"status": False, "message":"Une erreur s'est produite lors de l'opération, veuillez recommencer !"})
        




def paye_produit(request):
    if request.method == "POST":
        datas = request.POST
        try:
            for item in datas["tableau"].split(","):
                if "=" in item:
                    id, price = item.split("=")
                    PayeBrique.objects.filter(id=id).update(price = price)


            for item in datas["tableau1"].split(","):
                if "=" in item:
                    id, price = item.split("=")
                    PayeBrique.objects.filter(id=id).update(price_rangement = price)


            for item in datas["tableau2"].split(","):
                if "=" in item:
                    id, price = item.split("=")
                    PayeBrique.objects.filter(id=id).update(price_livraison = price)

                    
            return JsonResponse({"status": True})

        except Exception as e:
            print("--------------------", e)
            return JsonResponse({"status": False, "message":"Une erreur s'est produite lors de l'opération, veuillez recommencer !"})
        


def paye_produit_ferie(request):
    if request.method == "POST":
        datas = request.POST
        try:
            for item in datas["tableau"].split(","):
                if "=" in item:
                    id, price = item.split("=")
                    PayeBriqueFerie.objects.filter(id=id).update(price = price)


            for item in datas["tableau1"].split(","):
                if "=" in item:
                    id, price = item.split("=")
                    PayeBriqueFerie.objects.filter(id=id).update(price_rangement = price)


            for item in datas["tableau2"].split(","):
                if "=" in item:
                    id, price = item.split("=")
                    PayeBriqueFerie.objects.filter(id=id).update(price_livraison = price)
                    
            return JsonResponse({"status": True})

        except Exception as e:
            print("--------------------", e)
            return JsonResponse({"status": False, "message":"Une erreur s'est produite lors de l'opération, veuillez recommencer !"})
        