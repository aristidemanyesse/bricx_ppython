

from approvisionnementApp.models import Fournisseur
from clientApp.models import Client
from .models import CompteClient, ModePayement, Mouvement, TypeMouvement


def mouvement_pour_entree(request, datas, title, comment):
    mode = ModePayement.objects.get(pk = datas["modepayement"])
    type = TypeMouvement.objects.get(etiquette = TypeMouvement.DEPOT)

    montant = datas["montant"]
    montant = int(montant)

    if montant <= 0:
        return {"status":False, "message":"Le montant de l'opération est incorrect !"}
    if mode.etiquette == ModePayement.PRELEVEMENT :
        return {"status":False, "message":"Vous ne pouvez pas choisir ce mode de payement pour cette opération !"}
        
    return Mouvement.objects.create(
        name      = title,
        comment      = comment,
        montant   = montant,
        compte    = request.agence_compte,
        type      = type,
        mode      = mode,
        employe   = request.user.employe,
        structure = datas["structure"] or "",
        numero    = datas["numero"] or ""
    )
    



def mouvement_pour_sortie(request, datas, title, comment):
    mode = ModePayement.objects.get(pk = datas["modepayement"])
    type = TypeMouvement.objects.get(etiquette = TypeMouvement.RETRAIT)
    compte = request.agence_compte

    montant = datas["montant"]
    montant = int(montant)
    
    if montant <= 0:
        return {"status":False, "message":"Le montant de l'opération est incorrect !"}
    if mode.etiquette == ModePayement.PRELEVEMENT :
        return {"status":False, "message":"Vous ne pouvez pas choisir ce mode de payement pour cette opération !"}
    if compte.solde_actuel() < montant:
        return {"status":False, "message":"Fonds insuffisant pour effectuer cette opération!"}

    return Mouvement.objects.create(
        name      = title,
        comment      = comment,
        montant   = montant,
        compte    = compte,
        type      = type,
        mode      = mode,
        employe   = request.user.employe,
        structure = datas["structure"] or "",
        numero    = datas["numero"] or ""
    )
    



def mouvement_pour_sortie_client(request, datas, title, comment):
    try:
        mode = ModePayement.objects.get(pk = datas["modepayement"])
        type = TypeMouvement.objects.get(etiquette = TypeMouvement.RETRAIT)
        client = Client.objects.get(pk = request.session["client_id"])
        compte = request.agence_compte

        montant = datas["montant"]
        montant = int(montant)

        if montant <= 0:
            return {"status":False, "message":"Le montant de l'opération est incorrect !"}
        if mode.etiquette == ModePayement.PRELEVEMENT :
            if client.acompte_actuel() < montant:
                return {"status":False, "message":"L'acompte du client est insuffisant pour effectuer cette opération!"}
        # if compte.solde_actuel() < montant:
        #     return {"status":False, "message":"Fonds insuffisant pour effectuer cette opération!"}

        mouvement = Mouvement.objects.create(
            name      = title,
            comment   = comment,
            montant   = montant,
            compte    = compte,
            type      = type,
            mode      = mode,
            employe   = request.user.employe,
            structure = datas["structure"] or "",
            numero    = datas["numero"] or ""
        )

        return mouvement
    except Exception as e:
        print("-++++++++++++++++++++++++++++++", e)
        return {"status":False, "message":"Erreur lors de l'opération, veuillez recommencer!"}


    

def mouvement_pour_sortie_fournisseur(request, datas, title, comment):
    try:
        mode = ModePayement.objects.get(pk = datas["modepayement"])
        type = TypeMouvement.objects.get(etiquette = TypeMouvement.DEPOT)
        fournisseur = Fournisseur.objects.get(pk = request.session["fournisseur_id"])
        compte = request.agence_compte

        montant = datas["montant"]
        montant = int(montant)

        if montant <= 0:
            return {"status":False, "message":"Le montant de l'opération est incorrect !"}
        if mode.etiquette == ModePayement.PRELEVEMENT :
            if fournisseur.acompte_actuel() < montant:
                return {"status":False, "message":"Votre acompte chez le fournisseur est insuffisant pour effectuer cette opération!"}
        else:
            if compte.solde_actuel() < montant:
                return {"status":False, "message":"Fonds insuffisant pour effectuer cette opération!"}

        mouvement = Mouvement.objects.create(
            name      = title,
            comment   = comment,
            montant   = montant,
            compte    = compte,
            type      = type,
            mode      = mode,
            employe   = request.user.employe,
            structure = datas["structure"] or "",
            numero    = datas["numero"] or ""
        )

        return mouvement
    except Exception as e:
        print("-++++++++++++++++++++++++++++++", e)
        return {"status":False, "message":"Erreur lors de l'opération, veuillez recommencer!"}

