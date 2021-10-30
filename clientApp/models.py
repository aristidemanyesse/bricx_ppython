from django.db import models
from comptabilityApp.models import CompteClient, ModePayement, TypeMouvement
from django.db.models import Avg, Sum
from coreApp.models import BaseModel, Etat
from commandeApp.models import GroupeCommande, Commande
# Create your models here.



class TypeClient(BaseModel):
    PARTICULIER = "PARTICULIER"
    ENTREPRISE = "ENTREPRISE"

    name           = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255, null = True, blank=True)


class Client(BaseModel):
    name        = models.CharField(max_length = 255, null = False, blank=False)
    adresse         = models.CharField(max_length = 255, null = True, blank=True)
    email            = models.EmailField(max_length = 255, null = True, blank=True)
    contact         = models.CharField(max_length = 255, null = True, blank=True)
    acompte_initial = models.IntegerField(default=0, null = True, blank=True)
    dette_initial   = models.IntegerField(default=0, null = True, blank=True)
    seuil_credit    = models.IntegerField(default=0, null = True, blank=True)
    agence          = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="client_agence")
    type            = models.ForeignKey(TypeClient, on_delete = models.CASCADE, related_name="type_client")


    def acompte_actuel(self):
        total = 0
        datas = self.client_compte.filter(mouvement__type__etiquette = TypeMouvement.ENTREE).aggregate(Sum("mouvement__montant"))
        total += datas["mouvement__montant__sum"] or 0
        datas = self.client_compte.filter(mouvement__type__etiquette = TypeMouvement.SORTIE).aggregate(Sum("mouvement__montant"))
        total -= datas["mouvement__montant__sum"] or 0
        return self.acompte_initial + total


    def dette_totale(self):
        total = 0
        for commande in Commande.objects.filter(groupecommande__client = self, deleted = False):
            total += commande.reste_a_payer()

        datas = self.client_compte.filter(is_dette = True, mouvement__type__etiquette = TypeMouvement.SORTIE).aggregate(Sum("mouvement__montant"))
        total -= datas["mouvement__montant__sum"] or 0
        return self.dette_initial + total


    @staticmethod
    def dette_clients(agence):
        total = 0
        for client in Client.objects.filter(deleted = False, agence = agence):
            total += client.dette_totale()
        return total


    def get_groupecommandes(self):
        return self.client_groupecommande.filter(client = self).exclude(etat__etiquette = Etat.ANNULE).order_by("etat__etiquette", "-created_at", "datelivraison")


