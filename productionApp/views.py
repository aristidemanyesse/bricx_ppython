from django.shortcuts import render
from .models import Brique, Production, Ressource, LigneProduction, LigneConsommation
import datetime
# Create your views here.


def productions(request):
	if request.method == "GET":
		if 'tab' in request.session:
			del request.session['tab']
			
		briques = Brique.objects.filter(deleted = False)
		ressources = Ressource.objects.filter(deleted = False)
		try:
			productionday = Production.objects.get(date = datetime.datetime.now().date())
		except Exception as e:
			productionday = Production.objects.create(
				agence = request.agence,
				employe = request.user.employe,
				date = datetime.datetime.now().date()
			)

		context = {
			"productions" : Production.objects.filter(deleted = False, date__range = (request.session["date1"], request.session["date2"])),
			"productionday" : productionday,
			"briques" : briques,
			"ressources" : ressources
		}
		return render(request, "production/pages/productions.html", context)




def stock_brique(request):
	if request.method == "GET":
		context = {
			"briques" : Brique.objects.filter(deleted = False, active=True)
		}
		return render(request, "production/pages/stock_brique.html", context)