from django.urls import path

from .views import (
    VehiculeCreateView,
    VehiculeListView,
    VehiculeUpdateView,
    VehiculeDeleteView
)

app_name = "vehicules"

urlpatterns = [
    path("create/", VehiculeCreateView.as_view(), name="create"),
    path("list/", VehiculeListView.as_view(), name="list"),
    path("update/<int:pk>/", VehiculeUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", VehiculeDeleteView.as_view(), name="delete"),
]