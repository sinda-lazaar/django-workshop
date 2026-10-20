
from django.contrib import admin, messages
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Expedition


class EnRetardFilter(admin.SimpleListFilter):
    title = "En retard"
    parameter_name = "en_retard"

    def lookups(self, request, model_admin):
        return [
            ("oui", "Oui"),
            ("non", "Non"),
        ]

    def queryset(self, request, queryset):
        retard = queryset.filter(
            statut="publiee",
            date_souhaitee__lt=timezone.now().date()
        )

        if self.value() == "oui":
            return retard

        if self.value() == "non":
            return queryset.exclude(
                pk__in=retard.values("pk")
            )

        return queryset


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):

    list_display = (
        "reference",
        "ville_depart",
        "ville_arrive",
        "date_souhaitee",
        "poids_kg",
        "statut",
        "entreprise",
    )

    list_filter = (
        "statut",
        EnRetardFilter,
        "date_souhaitee",
    )

    search_fields = (
        "reference",
        "ville_depart",
        "ville_arrive",
    )

    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 10

    fieldsets = (
        (
            "Identité de l'expédition",
            {
                "fields": (
                    "reference",
                    "description",
                    "statut",
                )
            },
        ),
        (
            "Informations du trajet",
            {
                "fields": (
                    "ville_depart",
                    "ville_arrive",
                    "date_souhaitee",
                )
            },
        ),
        (
            "Informations sur la marchandise",
            {
                "fields": (
                    "poids_kg",
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

    readonly_fields = (
        "reference",
        "created_at",
        "updated_at",
    )

    @admin.action(
        description="Clôturer les expéditions sélectionnées"
    )
    def make_it_livree(self, request, queryset):
        # Seules les expéditions en cours peuvent être clôturées.
        liste = queryset.filter(statut="en_cours")

        nombre_eligibles = liste.count()
        nombre_ignores = queryset.count() - nombre_eligibles
        compteur = 0
        errors = []

        for exp in liste:
            exp.statut = "livree"

            try:
                exp.save()
                compteur += 1

            except ValidationError as error:
                errors.append(
                    f"{exp.reference} : "
                    f"erreur lors de la modification du statut : "
                    f"{', '.join(error.messages)}"
                )

        if compteur:
            self.message_user(
                request,
                f"{compteur} expédition(s) clôturée(s) avec succès.",
                messages.SUCCESS,
            )

        if nombre_ignores:
            self.message_user(
                request,
                f"{nombre_ignores} expédition(s) ignorée(s), "
                "car leur statut n'est pas « en cours ».",
                messages.WARNING,
            )

        for erreur in errors:
            self.message_user(
                request,
                erreur,
                messages.ERROR,
            )

        if nombre_eligibles == 0 and nombre_ignores == 0:
            self.message_user(
                request,
                "Aucune expédition sélectionnée.",
                messages.INFO,
            )

    actions = ["make_it_livree"]
