from django.urls import reverse
from commandeApp.models import Commande
from django.http import  JsonResponse
from comptabilityApp.models import CategoryOperation, Operation, ReglementAchatStock, ReglementApprovisionnement, Mouvement, ModePayement, CompteFournisseur
from comptabilityApp.tools import mouvement_pour_entree, mouvement_pour_sortie, mouvement_pour_sortie_fournisseur
from approvisionnementApp.models import AchatStock, Approvisionnement, Fournisseur
from authApp.tools import verify_password
from coreApp.models import Etat
# Create your views here.


def crediter(request):
    if request.method == "POST":
        datas = request.POST
        fournisseur = Fournisseur.objects.get(pk = request.session["fournisseur_id"])
        title = "Apport acompte fournisseur"
        comment = "Dépot d'acompte chez le fourniseur "+fournisseur.fullname +" d'un montant de "+datas["montant"]
        
        res = mouvement_pour_sortie(request, datas, title, comment)
        if type(res) is Mouvement:
            CompteFournisseur.objects.create(
                mouvement = res,
                fournisseur = fournisseur
            )
        else:
            return JsonResponse(res)
            
    return JsonResponse({"status":True, "url" : reverse("fiches:boncaisse", args=[res.id]) })



def rembourser(request):
    if request.method == "POST":
        datas = request.POST
        try:
            fournisseur = Fournisseur.objects.get(pk = request.session["fournisseur_id"])
            title = "Remboursement par fourniseur"
            comment = "Remboursement par le fournisseur "+fournisseur.fullname

            res = mouvement_pour_entree(request, datas, title, comment)
            if type(res) is Mouvement:
                Operation.objects.create(
                    mouvement = res,
                    category = CategoryOperation.objects.get(etiquette = CategoryOperation.REFUND_FOURNISSEUR)
                )

                CompteFournisseur.objects.create(
                    mouvement = res,
                    fournisseur = fournisseur,
                )
            else:
                return JsonResponse(res)

            return JsonResponse({"status":True, "url" : reverse("fiches:boncaisse", args=[res.id]) })

        except Exception as e:
            print("-++++++++++++++++++++++++++++++", e)





def regler_toutes_dettes(request):
    try:
        if request.method == "POST":
            datas = {}
            fournisseur = Fournisseur.objects.get(pk = request.session["fournisseur_id"])
            mode = ModePayement.objects.get(etiquette = ModePayement.ESPECES)
            
            datas["password"] = request.POST["password"]
            datas["modepayement"] = mode.id
            datas["structure"] = ""
            datas["numero"] = ""

            if not verify_password(request, datas["password"]):
                return JsonResponse({"status":False, "message" : "Le mot de passe est incorrect !" })

            acompte = request.agence_compte.solde_actuel()
            dette = fournisseur.dette_totale()
            while not (acompte <= 0 or dette <= 0 ):
                for appro in Approvisionnement.objects.filter(fournisseur = fournisseur, deleted = False).exclude(etat__etiquette = Etat.ANNULE):
                    reste =  appro.reste_a_payer()
                    if reste > 0 and acompte > 0:
                        datas["montant"] = reste if acompte >= reste else acompte
                        title ="Reglement approvisionnement"
                        comment = "reglement de l'approvisonnement N°"+appro.reference
                        res = mouvement_pour_sortie(request, datas, title, comment)
                        if type(res) is Mouvement:
                            ReglementApprovisionnement.objects.create(
                                mouvement = res,
                                approvisionnement = appro
                            )
                            acompte = request.agence_compte.solde_actuel()
                            dette = fournisseur.dette_totale()
                            if acompte <= 0 or dette <= 0:
                                break
                        else:
                            return JsonResponse(res)
                    else:
                        break

                if acompte <= 0 or dette <= 0:
                    break
                            
                for achat in AchatStock.objects.filter(fournisseur = fournisseur, deleted = False).exclude(etat__etiquette = Etat.ANNULE):
                    reste =  achat.reste_a_payer()
                    if reste > 0 and acompte > 0:
                        datas["montant"] = reste if acompte >= reste else acompte
                        title ="Reglement achat de stock"
                        comment = "reglement de l'achat de stock N°"+achat.reference
                        res = mouvement_pour_sortie(request, datas, title, comment)
                        if type(res) is Mouvement:
                            ReglementAchatStock.objects.create(
                                mouvement = res,
                                achatstock = achat
                            )
                            acompte = request.agence_compte.solde_actuel()
                            dette = fournisseur.dette_totale()
                            if acompte <= 0 or dette <= 0:
                                break
                        else:
                            return JsonResponse(res)
                    else:
                        break

        return JsonResponse({"status":True})
        
    except Exception as e:
        print("-++++++++++++++++++++++++++++++", e)
        return JsonResponse({"status":False, "message":e})