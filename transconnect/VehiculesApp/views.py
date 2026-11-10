from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .forms import VehiculeForm
from .models import Vehicule


class VehiculeListView(ListView):
    model = Vehicule
    template_name = "vehicules/list.html"
    context_object_name = "vehicules"


class VehiculeCreateView(CreateView):
    model = Vehicule
    form_class = VehiculeForm
    template_name = "vehicules/form.html"
    success_url = reverse_lazy("vehicules:list")


class VehiculeUpdateView(UpdateView):
    model = Vehicule
    form_class = VehiculeForm
    template_name = "vehicules/form.html"
    success_url = reverse_lazy("vehicules:list")


class VehiculeDeleteView(DeleteView):
    model = Vehicule
    template_name = "vehicules/confirm_delete.html"
    context_object_name = "vehicule"
    success_url = reverse_lazy("vehicules:list")
