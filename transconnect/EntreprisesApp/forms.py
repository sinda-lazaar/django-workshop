
from django import forms
from .models import Entreprise


class EntrepriseForm(forms.ModelForm):

    class Meta:
        model = Entreprise
        fields = [
            "raison_social",
            "matricule_fiscal",
            "type_entreprise",
            "adresse",
            "gerant",
        ]

        widgets = {
            "raison_social": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "matricule_fiscal": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "type_entreprise": forms.Select(
                attrs={"class": "form-control"}
            ),
            "adresse": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "gerant": forms.Select(
                attrs={"class": "form-control"}
            ),
        }
