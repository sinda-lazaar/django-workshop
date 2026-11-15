
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .models import Expedition
from .forms import ExpeditionForm


class ListeViewExpedition(ListView):
    model = Expedition
    template_name = "expeditions/liste.html"
    context_object_name = "expeditions"

    def get_queryset(self):
        return Expedition.objects.select_related(
            "entreprise"
        ).order_by("-created_at")


class ExpeditionDetailView(DetailView):
    model = Expedition
    template_name = "expeditions/detail.html"
    context_object_name = "expedition"
    slug_field = "reference"
    slug_url_kwarg = "reference"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["offres"] = self.object.offres.select_related(
            "transporteur", "vehicule"
        ).order_by("-date_proposition")

        return context


class ExpeditionCreateView(CreateView):
    model = Expedition
    form_class = ExpeditionForm
    template_name = "expeditions/form.html"
    success_url = reverse_lazy("expeditions:crud_list")


class ExpeditionUpdateView(UpdateView):
    model = Expedition
    form_class = ExpeditionForm
    template_name = "expeditions/form.html"
    success_url = reverse_lazy("expeditions:crud_list")


class ExpeditionDeleteView(DeleteView):
    model = Expedition
    template_name = "expeditions/confirm_delete.html"
    context_object_name = "expedition"
    success_url = reverse_lazy("expeditions:crud_list")
