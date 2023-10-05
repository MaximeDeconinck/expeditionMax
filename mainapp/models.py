from django.db import models

class Travel(models.Model):
    date = models.DateField()
    heure_depart = models.TimeField()
    heure_arrivee = models.TimeField()
    origine = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

class Expedition(models.Model):
    travel_go = models.ForeignKey(Travel, related_name='expedition_aller', on_delete=models.CASCADE)
    travel_back = models.ForeignKey(Travel, related_name='expedition_retour', on_delete=models.CASCADE)