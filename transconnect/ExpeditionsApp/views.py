from django.views.generic import DetailView, ListView

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


class ExpeditionDetailView(DetailView):
    model = Expedition
    template_name = "expeditions/detail.html"
    context_object_name = "expedition"

    slug_field = "reference"
    slug_url_kwarg = "reference"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["offres"] = (
            self.object.offres
            .select_related("transporteur", "vehicule")
            .order_by("-date_proposition")
        )

        return context
