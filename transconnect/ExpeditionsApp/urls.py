
from django.urls import path

from .views import (
    ListeViewExpedition,
    ExpeditionDetailView,
    ExpeditionCreateView,
    ExpeditionUpdateView,
    ExpeditionDeleteView,
)

app_name = "expeditions"

urlpatterns = [
    # CRUD : placer ces routes AVANT la route dynamique
    path("crud/", ListeViewExpedition.as_view(), name="crud_list"),
    path("create/", ExpeditionCreateView.as_view(), name="create"),
    path("update/<int:pk>/", ExpeditionUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ExpeditionDeleteView.as_view(), name="delete"),

    # Consultation publique
    path("", ListeViewExpedition.as_view(), name="liste"),
    path("<str:reference>/", ExpeditionDetailView.as_view(), name="detail"),
]
