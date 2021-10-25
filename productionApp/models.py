
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import Sum, Avg
import commandeApp.models 
from coreApp.models import BaseModel, Etat
import uuid, datetime

from organisationApp.models import Agence

# Create your models here.

class TypePerte(BaseModel):
    CHARGEMENT      = 1
    DECHARGEMENT = 2
    
    name      = models.CharField(max_length = 255)
    etiquette = models.CharField(max_length = 255)


class Brique(BaseModel):
    name      = models.CharField(max_length = 255)
    active = models.BooleanField(default=True)
    comment   = models.TextField(default="", null = True, blank=True)
    alert_stock         = models.IntegerField(default=10)
    image     = models.ImageField(max_length = 255, upload_to = "storage/images/briques/", default="", null = True, blank=True)


    def stock(self, agence, fin=None):
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        return self.attente(agence, fin) + self.livrable(agence, fin)

    def attente(self, agence, fin=None):
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        res = self.brique_ligneproduction.filter(deleted = False, production__created_at__lte = fin, production__etat__etiquette = Etat.EN_COURS).aggregate(Sum('quantite'))
        return res["quantite__sum"] or 0

    def livrable(self, agence, fin=None):
        debut = datetime.date.fromisoformat("2021-06-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        initial = self.brique_initialagence.filter(deleted = False, agence = agence).aggregate(Sum('quantite'))
        return (initial["quantite__sum"] or 0) + self.production(agence, None, fin) + self.achat(agence, None, fin) - self.livraison(agence, None, fin) - self.perte(agence, None, fin) - self.surplus(agence, fin) - self.attente(agence, fin);

    def production(self, agence, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-06-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        print(debut, fin)
        res = self.brique_ligneproduction.filter(deleted = False, production__created_at__range = (debut, fin)).exclude(production__etat__etiquette = Etat.ANNULE).aggregate(Sum('quantite'))
        return res["quantite__sum"] or 0




    def livraison(self, agence, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-06-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        res = self.brique_lignelivraison.filter(deleted = False, livraison__created_at__range = (debut, fin)).exclude(livraison__etat__etiquette = Etat.ANNULE).aggregate(Sum('quantite'))
        return res["quantite__sum"] or 0

    def surplus(self, agence, fin=None):
        res = self.brique_lignelivraison.filter(deleted = False, livraison__created_at__lte = fin, livraison__etat__etiquette = Etat.EN_COURS).aggregate(Sum('surplus'))
        return res["surplus__sum"] or 0
        
    def achat(self, agence, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-06-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        res = self.brique_ligneachatstock.filter(deleted = False, achatstock__created_at__range = (debut, fin)).exclude(achatstock__etat__etiquette = Etat.ANNULE).aggregate(Sum('quantite'))
        return res["quantite__sum"] or 0


    def perte(self, agence, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-06-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        return self.perte_livraison(agence, debut, fin) + self.perte_autre(agence, debut, fin) + self.perte_rangement(agence, debut, fin)

    def perte_chargement(self, agence, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-06-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        res = self.brique_perte.filter(deleted = False, created_at__range = (debut, fin), type__etiquette = TypePerte.CHARGEMENT).aggregate(Sum('quantite'))
        return res["quantite__sum"] or 0

    def perte_dechargement(self, agence, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-06-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        res = self.brique_perte.filter(deleted = False, created_at__range = (debut, fin), type__etiquette = TypePerte.DECHARGEMENT).aggregate(Sum('quantite'))
        return res["quantite__sum"] or 0

    def perte_autre(self, agence, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-06-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        res = self.brique_perte.filter(deleted = False, created_at__range = (debut, fin)).exclude(type__etiquette = TypePerte.CHARGEMENT).exclude(type__etiquette = TypePerte.DECHARGEMENT).aggregate(Sum('quantite'))
        return res["quantite__sum"] or 0

    def perte_rangement(self, agence, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-06-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        res = self.brique_ligneproduction.filter(deleted = False, production__created_at__range = (debut, fin)).exclude(production__etat__etiquette = Etat.ANNULE).aggregate(Sum('perte'))
        return res["perte__sum"] or 0

    def perte_livraison(self, agence, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-06-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        return self.perte_chargement(agence, debut, fin) + self.perte_dechargement(agence, debut, fin)


    def estimation(self, quantite, ressource):
        return 100


    def exigence(self, quantite, ressource):
        try:
            exigence = self.brique_exigenceproduction.get()
            ligne = LigneExigenceProduction.objects.get(exigence = exigence, ressource = ressource)
            if int(quantite) > 0:
                return (quantite * ligne.quantite) / exigence.quantite;
            return 0
        except:
            return 0


    def cout(self, type, quantite, isferie = False):
        try:
            if quantite >= 0:
                if isferie:
                    paye = self.brique_paye.get()
                else:
                    paye = self.brique_payeferie.get()

                if type == "production":
                    price = paye.price
                elif type == "rangement":
                    price = paye.price_rangement
                elif type == "livraison":
                    price = paye.priprice_livraisonce
                    
                return quantite * price;
            return 0  
        except:
            return 0  


class Ressource(BaseModel):
    name      = models.CharField(max_length = 255)
    unite      = models.CharField(max_length = 255, default="")
    active = models.BooleanField(default=True)
    alert_stock         = models.IntegerField(default=10)
    comment   = models.TextField(default="", null = True, blank=True)
    image     = models.ImageField(max_length = 255, upload_to = "storage/images/ressources/", default="", null = True, blank=True)

    
    def stock(self, agence, fin=None):
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        initial = self.ressource_initialagence.filter(deleted = False, agence = agence).aggregate(Sum('quantite'))
        return (initial["quantite__sum"] or 0) + self.achat(agence, None, fin) - self.consommation(agence, None, fin) - self.perte(agence, None, fin)

    def consommation(self, agence, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-06-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        print(debut, fin)
        res = self.ressource_ligneconsommation.filter(deleted = False, production__created_at__range = (debut, fin)).exclude(production__etat__etiquette = Etat.ANNULE).aggregate(Sum('quantite'))
        return res["quantite__sum"] or 0

    def achat(self, agence, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-06-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        res = self.ressource_ligneapprovisionnement.filter(deleted = False, approvisionnement__created_at__range = (debut, fin), approvisionnement__etat__etiquette = Etat.TERMINE).aggregate(Sum('quantite'))
        return res["quantite__sum"] or 0

    def perte(self, agence, debut=None, fin=None):
        debut = debut or datetime.date.fromisoformat("2021-06-01")
        fin = fin or datetime.date.today() + datetime.timedelta(days=1)
        res = self.ressource_perte.filter(deleted = False, created_at__range = (debut, fin)).aggregate(Sum('quantite'))
        return res["quantite__sum"] or 0


    def estimation(self, quantite, ressource):
        return 100


class Production(BaseModel):
    reference          = models.CharField(max_length = 255)
    agence             = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_production")
    employe            = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_production")
    employe_rangement  = models.ForeignKey("organisationApp.Employe",  null = True, blank=True, on_delete = models.CASCADE, related_name="employe_rangement_production")
    date               = models.DateField(null = True, blank=True,)
    date_rangement     = models.DateTimeField(null = True, blank=True)
    etat               = models.ForeignKey("coreApp.Etat", on_delete = models.CASCADE)
    montant_production = models.IntegerField(default=0)
    montant_rangement  = models.IntegerField(default=0)
    montant_livraison  = models.IntegerField(default=0)
    comment            = models.TextField(default="", null = True, blank=True)

    def __str__(self):
        return "production du "+str(self.date)

class LigneProduction(BaseModel):
    production = models.ForeignKey(Production, on_delete = models.CASCADE, related_name="production_ligne")
    brique     = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_ligneproduction")
    perte      = models.IntegerField(default=0)
    quantite   = models.IntegerField(default=0)

    def __str__(self):
        return "production du "+str(self.production.date)+" : "+self.brique.name+" => "+str(self.quantite)

class LigneConsommation(BaseModel):
    production = models.ForeignKey(Production, on_delete = models.CASCADE, related_name="production_ligneconsommation")
    ressource  = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_ligneconsommation")
    quantite   = models.IntegerField(default = 0)

    def __str__(self):
        return "consommation du "+str(self.production.date)+" : "+self.ressource.name+" => "+str(self.quantite)


class ConsommationJour(BaseModel):
    date        = models.DateField(default="", null = True, blank=True)
    comment     = models.TextField(default="", null = True, blank=True)
    employe = models.ForeignKey("organisationApp.Employe",  null = True, blank=True, on_delete = models.CASCADE, related_name="employe_consommationjour")



class ExigenceProduction(BaseModel):
    brique   = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_exigenceproduction")
    quantite = models.IntegerField(default=0)


class LigneExigenceProduction(BaseModel):
    exigence  = models.ForeignKey(ExigenceProduction, on_delete = models.CASCADE, related_name="exigence_ligne")
    ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_exigenceligne")
    quantite  = models.IntegerField(default = 0)



class InitialBriqueAgence(BaseModel):
    agence   = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_initialbrique")
    brique   = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_initialagence")
    quantite = models.IntegerField(default=0)


class InitialRessourceAgence(BaseModel):
    agence    = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_initialressource")
    ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_initialagence")
    quantite  = models.IntegerField(default=0)



class PerteRessource(BaseModel):
    type        = models.ForeignKey(TypePerte, on_delete = models.CASCADE, related_name="type_perteressource")
    agence      = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_perteressource")
    ressource   = models.ForeignKey(Ressource, on_delete = models.CASCADE, related_name="ressource_perte")
    employe = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_perteressource")
    quantite    = models.IntegerField(default=0)
    comment     = models.TextField(default="",  null = True, blank=True)

    def __str__(self):
        return " perte de " + str(self.quantite) + " " +self.ressource.unite +" de " +self.ressource.name

class PerteBrique(BaseModel):
    type        = models.ForeignKey(TypePerte, on_delete = models.CASCADE, related_name="type_pertebrique")
    agence      = models.ForeignKey("organisationApp.Agence", on_delete = models.CASCADE, related_name="agence_perte")
    brique      = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_perte")
    employe = models.ForeignKey("organisationApp.Employe", on_delete = models.CASCADE, related_name="employe_pertebrique")
    quantite    = models.IntegerField(default=0)
    comment     = models.TextField(default="",  null = True, blank=True)

    def __str__(self):
        return str(self.quantite) + " perte de " +self.brique.name


class PayeBrique(BaseModel):
    brique          = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_paye")
    price           = models.IntegerField(default=0)
    price_rangement = models.IntegerField(default=0)
    price_livraison = models.IntegerField(default=0)


class PayeBriqueFerie(BaseModel):
    brique = models.ForeignKey(Brique, on_delete = models.CASCADE, related_name="brique_payeferie")
    price = models.IntegerField(default=0)
    price_rangement = models.IntegerField(default=0)
    price_livraison = models.IntegerField(default=0)


######################################################################################################
##### SIGNAUX



@receiver(pre_save, sender = Production)
def pre_save_production(sender, instance, **kwargs):
    if instance._state.adding:
        instance.etat = Etat.objects.get(etiquette = Etat.EN_COURS)
        instance.reference = uuid.uuid4()




@receiver(post_save, sender = Production)
def post_save_production(sender, instance, created, **kwargs):
    if created:
        for brique in Brique.objects.filter(deleted = False, active = True):
            LigneProduction.objects.create(
            production = instance,
            brique = brique
        )
            
        for ressource in Ressource.objects.filter(deleted = False, active = True):
            LigneConsommation.objects.create(
                production = instance,
                ressource = ressource
            )




@receiver(post_save, sender = Brique)
def post_save_brique(sender, instance, created, **kwargs):
    if created:
        for zone in commandeApp.models.ZoneLivraison.objects.filter(deleted = False):
            commandeApp.models.PrixZoneLivraison.objects.create(
                brique = instance,
                zone = zone,
                price = 0
            )

        for agence in Agence.objects.filter(deleted = False):
            InitialBriqueAgence.objects.create(
                brique = instance,
                agence = agence,
                quantite = 0
            )

        ExigenceProduction.objects.create(
            brique = instance,
            quantite = 0
        )

        PayeBrique.objects.create(
            brique = instance,
            price = 0
        )

        PayeBriqueFerie.objects.create(
            brique = instance,
            price = 0
        )



@receiver(post_save, sender = Ressource)
def post_save_ressource(sender, instance, created, **kwargs):
    if created:

        for agence in Agence.objects.filter(deleted = False):
            InitialRessourceAgence.objects.create(
                ressource = instance,
                agence = agence,
                quantite = 0
            )

        for exigence in ExigenceProduction.objects.filter(deleted = False):
            LigneExigenceProduction.objects.create(
                exigence = exigence,
                ressource = instance,
                quantite = 0
            )




@receiver(pre_save, sender = PerteBrique)
def pre_save_perte_brique(sender, instance, **kwargs):
    if instance._state.adding:
        if instance.brique.stock(instance.agence) < instance.quantite:
            raise Exception("Vous ne pouvez déclarer de perte au délà du stock disponible")


@receiver(pre_save, sender = PerteRessource)
def pre_save_perte_ressource(sender, instance, **kwargs):
    if instance._state.adding:
        if instance.ressource.stock(instance.agence) < instance.quantite:
            raise Exception("Vous ne pouvez déclarer de perte au délà du stock disponible")