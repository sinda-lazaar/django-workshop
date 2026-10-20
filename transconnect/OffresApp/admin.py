
from django.contrib import admin
from django.utils.html import format_html
from .models import Offre


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "prix",
        "date_proposition",
        "delai_jours",
        "statut_colore",
        "transporteur",
        "expedition",
        "vehicule",
    )

    list_filter = (
        "statut",
        "date_proposition",
    )

    search_fields = (
        "transporteur__id",
        "expedition__id",
        "vehicule__immatriculation",
    )

    ordering = ("-date_proposition",)
    date_hierarchy = "date_proposition"
    list_per_page = 10

    @admin.display(description="Statut")
    def statut_colore(self, obj):
        couleurs = {
            "proposee": "#F0AD4E",
            "acceptee": "#5CB85C",
            "refusee": "#D9534F",
            "retiree": "#777777",
        }

        return format_html(
            '<span style="color:white; background:{}; '
            'padding:3px 8px; border-radius:4px;">{}</span>',
            couleurs.get(obj.statut, "#999999"),
            obj.get_statut_display(),
        )

    fieldsets = (
        (
            "Informations de l'offre",
            {
                "fields": (
                    "prix",
                    "delai_jours",
                    "statut",
                )
            },
        ),
        (
            "Transport et expédition",
            {
                "fields": (
                    "transporteur",
                    "expedition",
                    "vehicule",
                )
            },
        ),
        (
            "Dates système",
            {
                "fields": (
                    "date_proposition",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    readonly_fields = (
        "date_proposition",
        "created_at",
        "updated_at",
    )
