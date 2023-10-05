from django.shortcuts import render, redirect
from .models import Travel, Expedition
from django.db.models import F
from django.http import HttpResponse, JsonResponse
import requests, json
from itertools import groupby
from .forms import SearchExpeditionsForm

def index(request):
    return render(request, 'index.html')

def travels(request):
    travels = Travel.objects.all()
    count = travels.count()
    context = {
        'travels': travels,
        'count': count,
        }
    return render(request, 'travels.html', context)

def save_travels_from_api(request):
    url = "https://data.sncf.com/api/records/1.0/search/?dataset=tgvmax&q=&rows=2000&facet=date&facet=origine&facet=destination&facet=od_happy_card&refine.od_happy_card=OUI"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        for record in data["records"]:
            travel = {
                "date": record["fields"]["date"],
                "origine": record["fields"]["origine"],
                "heure_arrivee": record["fields"]["heure_arrivee"],
                "destination": record["fields"]["destination"],
                "heure_depart": record["fields"]["heure_depart"],
            }

            Travel.objects.get_or_create(
                date=travel["date"],
                origine=travel["origine"],
                heure_arrivee=travel["heure_arrivee"],
                destination=travel["destination"],
                heure_depart=travel["heure_depart"],
            )

        return redirect('travels')
    return redirect('travels')

def delete_travels(request):
    Travel.objects.all().delete()
    return redirect('travels')

def expeditions(request):
    expeditions = Expedition.objects.all().order_by('travel_go__origine')
    count = expeditions.count()
    context = {
        'expeditions': expeditions,
        'count': count,
        }
    return render(request, 'expeditions.html', context)

def calculate_expeditions(request):
    travels = Travel.objects.all()
    expeditions = []

    travels_sorted = sorted(travels, key=lambda x: x.origine)

    for travel_aller in travels_sorted:
        matching_travels_retour = travels.filter(
            date__gt=travel_aller.date,
            destination=travel_aller.origine,
            origine=travel_aller.destination
        )

        for travel_retour in matching_travels_retour:
            expedition = Expedition.objects.get_or_create(travel_go=travel_aller, travel_back=travel_retour)
            expeditions.append(expedition)

    return redirect('expeditions')

def delete_expeditions(request):
    Expedition.objects.all().delete()
    return redirect('expeditions')

def search_expeditions(request):
    origin_cities = Expedition.objects.values_list('travel_go__origine', flat=True).distinct()
    
    if request.method == 'POST':
        form = SearchExpeditionsForm(request.POST)
        if form.is_valid():
            origin_city = form.cleaned_data['origin_city']
            expeditions = Expedition.objects.filter(
                travel_go__origine=origin_city,
                travel_back__destination=origin_city
            )
    else:
        form = SearchExpeditionsForm()

    context = {
        'origin_cities': origin_cities,
        'form': form,
        'expeditions': expeditions if 'expeditions' in locals() else None,
        'origin_city': origin_city if 'origin_city' in locals() else None,
    }
    return render(request, 'search_expeditions.html', context)