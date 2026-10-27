
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Expedition


class ListeViewExpedition(ListView):
    model = Expedition
    template_name = "expeditions/liste.html"
    context_object_name = "expeditions"

    def get_queryset(self):
        return (
            Expedition.objects
            .filter(statut="publiee")
            .select_related("entreprise")
            .order_by("-created_at")
        )


def detail_expedition(request, reference):
    expedition = get_object_or_404(
        Expedition,
        reference=reference
    )

    offres = (
        expedition.offre
        .select_related("transporteur", "vehicule")
        .order_by("-date_proposition")
    )

    return render(
        request,
        "expeditions/detail.html",
        {
            "expedition": expedition,
            "offres": offres,
        },
    )
