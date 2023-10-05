from django import forms
from .models import Expedition

class SearchExpeditionsForm(forms.Form):
    origin_city = forms.ChoiceField(label='Ville d\'origine', choices=[])

    def __init__(self, *args, **kwargs):
        super(SearchExpeditionsForm, self).__init__(*args, **kwargs)
        origin_cities = Expedition.objects.values_list('travel_go__origine', flat=True).distinct()
        sorted_cities = sorted(origin_cities, key=lambda x: x.lower())  # Triez les villes en ordre alphabétique
        self.fields['origin_city'].choices = [(city, city) for city in sorted_cities]