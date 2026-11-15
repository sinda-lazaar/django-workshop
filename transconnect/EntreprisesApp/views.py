
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .models import Entreprise
from .forms import EntrepriseForm


class EntrepriseListView(ListView):
    model = Entreprise
    template_name = "entreprises/list.html"
    context_object_name = "entreprises"


class EntrepriseCreateView(CreateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = "entreprises/form.html"
    success_url = reverse_lazy("entreprises:list")


class EntrepriseUpdateView(UpdateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = "entreprises/form.html"
    success_url = reverse_lazy("entreprises:list")


class EntrepriseDeleteView(DeleteView):
    model = Entreprise
    template_name = "entreprises/confirm_delete.html"
    context_object_name = "entreprise"
    success_url = reverse_lazy("entreprises:list")


class EntrepriseDetailView(DetailView):
    model = Entreprise
    template_name = "entreprises/detail.html"
    context_object_name = "entreprise"
