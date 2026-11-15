
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .models import Offre
from .forms import OffreForm


class OffreListView(ListView):
    model = Offre
    template_name = "offres/list.html"
    context_object_name = "offres"


class OffreCreateView(CreateView):
    model = Offre
    form_class = OffreForm
    template_name = "offres/form.html"
    success_url = reverse_lazy("offres:list")


class OffreUpdateView(UpdateView):
    model = Offre
    form_class = OffreForm
    template_name = "offres/form.html"
    success_url = reverse_lazy("offres:list")


class OffreDeleteView(DeleteView):
    model = Offre
    template_name = "offres/confirm_delete.html"
    context_object_name = "offre"
    success_url = reverse_lazy("offres:list")


class OffreDetailView(DetailView):
    model = Offre
    template_name = "offres/detail.html"
    context_object_name = "offre"
