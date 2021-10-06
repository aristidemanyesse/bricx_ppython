from django.shortcuts import render
from commandeApp.models import PrixZoneLivraison

# Create your views here.
def prixparzone(request, id):
    if request.method == "GET":
        zone = get_object_or_404(ZoneLivraison, pk = id)
        context = {
                "zone" : zone,
                "prixparzones" : zone.zone_prix.filter(),
            }
        return render(request, "fiches/pages/prixparzone.html", context)