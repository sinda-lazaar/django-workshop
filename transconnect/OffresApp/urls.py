
from django.urls import path

from .views import (
    OffreListView,
    OffreCreateView,
    OffreUpdateView,
    OffreDeleteView,
    OffreDetailView,
)

app_name = "offres"

urlpatterns = [
    path("", OffreListView.as_view(), name="list"),

    path("create/", OffreCreateView.as_view(), name="create"),

    path("update/<int:pk>/",
         OffreUpdateView.as_view(), name="update"),

    path("delete/<int:pk>/",
         OffreDeleteView.as_view(), name="delete"),

    path("detail/<int:pk>/",
         OffreDetailView.as_view(), name="detail"),
]
