from django.urls import path
from .views import *
app_name='expeditions'
urlpatterns = [
    path("", liste_expeditions,name="liste"),
]