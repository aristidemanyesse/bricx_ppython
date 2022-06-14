import uuid
from django.contrib.auth.models import Permission
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from commandeApp.models import PrixZoneLivraison
import coreApp.tools as tools
from organisationApp.models import Employe
from paramApp.models import MyApp
from productionApp.models import ExigenceProduction, LigneExigenceProduction, PayeBrique, PayeBriqueFerie
from django.utils.translation import ugettext as _

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
            return JsonResponse({"status": False, "message":_("Une erreur s'est produite lors de l'opération, veuillez recommencer !")})
        
        

def change_production_auto(request):
    if request.method == "POST":
        datas = request.POST

        try:
            obj = MyApp.objects.filter().first()"message":
            obj.production_auto = not obj.production_auto
            obj.save()

            return JsonResponse({"status":True, "message":_("Suppression effectuée avec succes !")})

        except Exception as e:
            print("erreur save :", e)
            return JsonResponse({"status":False, "message":_("Erreur lors du processus. Veuillez recommencer : ")+str(e)})




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
            return JsonResponse({"status": False, "message":_("Une erreur s'est produite lors de l'opération, veuillez recommencer !")})
        




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
            return JsonResponse({"status": False, "message":_("Une erreur s'est produite lors de l'opération, veuillez recommencer !")})
        


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
            return JsonResponse({"status": False, "message":_("Une erreur s'est produite lors de l'opération, veuillez recommencer !")})
        




def permissions(request):
    if request.method == "POST":
        datas = request.POST
        try:
            perm = Permission.objects.get(pk = datas["perm_id"])
            employe = Employe.objects.get(pk = datas["employe_id"])

            if not employe.is_active:
                return JsonResponse({"status": False, "message":_("L'accès est déjà refusé à cet employé !")})
            if employe.is_staff:
                return JsonResponse({"status": False, "message":_("Vous ne pouvez pas supprimer cet accès, il est protégé !")})

            if datas["value"] == "true":
                employe.user_permissions.add(perm)
            else:
                employe.user_permissions.remove(perm)

            return JsonResponse({"status": True})

        except Exception as e:
            print("--------------------", e)
            return JsonResponse({"status": False, "message":_("Une erreur s'est produite lors de l'opération, veuillez recommencer !")})
        





def lock(request):
    if request.method == "POST":
        datas = request.POST
        try:
            employe = Employe.objects.get(pk = datas["id"])

            if "password" in datas and not request.user.check_password(datas["password"]):
                return JsonResponse({"status":False, "message":_("Le mot de passe est incorrect !")})

            if employe.is_staff:
                return JsonResponse({"status": False, "message":_("Vous ne pouvez pas supprimer cet utilisateur, il est protégé !")})
            if employe.is_active:
                employe.is_active = False
                employe.save()

            return JsonResponse({"status": True})

        except Exception as e:
            print("--------------------", e)
            return JsonResponse({"status": False, "message":_("Une erreur s'est produite lors de l'opération, veuillez recommencer !")})
        


def unlock(request):
    if request.method == "POST":
        datas = request.POST
        try:
            employe = Employe.objects.get(pk = datas["id"])

            if "password" in datas and not request.user.check_password(datas["password"]):
                return JsonResponse({"status":False, "message":_("Le mot de passe est incorrect !")})

            if employe.is_staff:
                return JsonResponse({"status": False, "message":_("Vous ne pouvez pas supprimer cet utilisateur, il est protégé !")})
            if not employe.is_active:
                employe.is_active = True
                employe.save()

            return JsonResponse({"status": True})

        except Exception as e:
            print("--------------------", e)
            return JsonResponse({"status": False, "message":_("Une erreur s'est produite lors de l'opération, veuillez recommencer !")})
        



def reset_password(request):
    if request.method == "POST":
        datas = request.POST
        try:
            employe = Employe.objects.get(pk = datas["id"])

            if "password" in datas and not request.user.check_password(datas["password"]):
                return JsonResponse({"status":False, "message":_("Le mot de passe est incorrect !")})

            if employe.is_staff:
                return JsonResponse({"status": False, "message":_("Vous ne pouvez pas supprimer cet utilisateur, il est protégé !")})
            if not employe.is_active:
                return JsonResponse({"status": False, "message":_("L'accès est déjà refusé à cet employé, veuillez d'abor le débloquer !")})

            employe.is_never_connected = True
            employe.username = str(uuid.uuid4()).split("-")[-1]
            employe.brut = str(uuid.uuid4()).split("-")[-1]
            employe.set_password(employe.brut)
            employe.save()

            return JsonResponse({"status": True})

        except Exception as e:
            print("--------------------", e)
            return JsonResponse({"status": False, "message":_("Une erreur s'est produite lors de l'opération, veuillez recommencer !")})
    
