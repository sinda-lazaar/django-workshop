
from django import forms
from .models import Offre


class OffreForm(forms.ModelForm):

    class Meta:
        model = Offre
        fields = [
            "prix",
            "delai_jours",
            "statut",
            "transporteur",
            "expedition",
            "vehicule",
        ]

        widgets = {
            "prix": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "delai_jours": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "statut": forms.Select(
                attrs={"class": "form-control"}
            ),
            "transporteur": forms.Select(
                attrs={"class": "form-control"}
            ),
            "expedition": forms.Select(
                attrs={"class": "form-control"}
            ),
            "vehicule": forms.Select(
                attrs={"class": "form-control"}
            ),
        }
