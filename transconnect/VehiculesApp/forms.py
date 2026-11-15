
from django import forms
from .models import Vehicule


class VehiculeForm(forms.ModelForm):

    class Meta:
        model = Vehicule

        fields = [
            "immatriculation",
            "type_vehicule",
            "capacite_kg",
            "disponible",
            "entreprise",
        ]

        widgets = {
            "immatriculation": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "type_vehicule": forms.Select(
                attrs={"class": "form-control"}
            ),

            "capacite_kg": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "disponible": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),

            "entreprise": forms.Select(
                attrs={"class": "form-control"}
            ),
        }
