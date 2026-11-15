
from django.urls import path

from .views import (
    VehiculeCreateView,
    VehiculeListView,
    VehiculeUpdateView,
    VehiculeDeleteView,
    VehiculeDetailView,
)

app_name = "vehicules"

urlpatterns = [
    path("list/", VehiculeListView.as_view(), name="list"),

    path("create/", VehiculeCreateView.as_view(), name="create"),

    path("detail/<int:pk>/",
         VehiculeDetailView.as_view(), name="detail"),

    path("update/<int:pk>/",
         VehiculeUpdateView.as_view(), name="update"),

    path("delete/<int:pk>/",
         VehiculeDeleteView.as_view(), name="delete"),
]
