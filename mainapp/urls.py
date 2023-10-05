from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('travels/', views.travels, name='travels'),
  path('save_travels_from_api', views.save_travels_from_api, name='save_travels_from_api'),
  path('delete_travels', views.delete_travels, name='delete_travels'),
  path('expeditions/', views.expeditions, name='expeditions'),
  path('calculate-expeditions', views.calculate_expeditions, name='calculate_expeditions'),
  path('delete_expeditions', views.delete_expeditions, name='delete_expeditions'),
  path('search_expeditions/', views.search_expeditions, name='search_expeditions'),
]