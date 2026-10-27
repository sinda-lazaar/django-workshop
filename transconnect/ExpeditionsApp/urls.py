
from django.urls import path
from .views import ListeViewExpedition, detail_expedition

app_name = 'expeditions'

urlpatterns = [
    path("", ListeViewExpedition.as_view(), name="liste"),
    path("<str:reference>/", detail_expedition, name="details_expedition"),
]
