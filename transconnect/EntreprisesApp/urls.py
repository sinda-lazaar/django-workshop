
from django.urls import path

from .views import (
    EntrepriseListView,
    EntrepriseCreateView,
    EntrepriseUpdateView,
    EntrepriseDeleteView,
    EntrepriseDetailView,
)

app_name = "entreprises"

urlpatterns = [
    path("", EntrepriseListView.as_view(), name="list"),

    path("create/", EntrepriseCreateView.as_view(), name="create"),

    path("update/<int:pk>/",
         EntrepriseUpdateView.as_view(), name="update"),

    path("delete/<int:pk>/",
         EntrepriseDeleteView.as_view(), name="delete"),

    path("detail/<int:pk>/",
         EntrepriseDetailView.as_view(), name="detail"),
]
