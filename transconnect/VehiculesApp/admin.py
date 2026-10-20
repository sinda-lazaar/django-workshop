
from django.contrib import admin
from .models import Vehicule


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):

    # Colonnes affichées dans la liste des véhicules
    list_display = (
        "id",
        "immatriculation",
        "type_vehicule",
        "capacite_kg",
        "disponible",
        "entreprise",
    )

    # Filtres disponibles
    list_filter = (
        "type_vehicule",
        "disponible",
    )

    # Recherche de véhicules
    search_fields = (
        "immatriculation",
        "type_vehicule",
        "entreprise__id",
    )

    # Tri par identifiant décroissant
    ordering = ("-id",)

    # Nombre de véhicules par page
    list_per_page = 10

    # Organisation du formulaire
    fieldsets = (
        (
            "Identité du véhicule",
            {
                "fields": (
                    "immatriculation",
                    "type_vehicule",
                    "capacite_kg",
                )
            },
        ),
        (
            "Disponibilité et entreprise",
            {
                "fields": (
                    "disponible",
                    "entreprise",
                )
            },
        ),
        (
            "Dates système",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    # Champs générés automatiquement
    readonly_fields = (
        "created_at",
        "updated_at",
    )
