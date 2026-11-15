
from django import forms
from .models import Expedition


class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = Expedition
        fields = [
            "ville_depart",
            "ville_arrive",
            "date_souhaitee",
            "poids_kg",
            "description",
            "statut",
            "entreprise",
        ]

        widgets = {
            "ville_depart": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "ville_arrive": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "date_souhaitee": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
            "poids_kg": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
            }),
            "statut": forms.Select(attrs={
                "class": "form-control",
            }),
            "entreprise": forms.Select(attrs={
                "class": "form-control",
            }),
        }
