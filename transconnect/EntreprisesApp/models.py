
import re

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils import timezone


def validate_gmail(value):
    """Accepte uniquement les adresses du domaine gmail.com."""
    if not value.lower().endswith("@gmail.com"):
        raise ValidationError(
            "L'adresse email doit appartenir au domaine gmail.com."
        )


matricule_validator = RegexValidator(
    regex=r"^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$",
    message="Format invalide du matricule fiscal tunisien."
)


class Utilisateur(AbstractUser):
    user_id = models.CharField(
        max_length=8,
        primary_key=True,
        editable=False
    )

    email = models.EmailField(
        unique=True,
        validators=[validate_gmail]
    )

    role = models.CharField(
        max_length=20,
        choices=[
            ("chargeur", "Chargeur"),
            ("transporteur", "Transporteur"),
            ("administrateur", "Administrateur"),
        ],
        default="chargeur"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    telephone = models.CharField(max_length=8)
    REQUIRED_FIELDS = ["email","telephone"]
    def save(self, *args, **kwargs):
        if not self.user_id:
            prefix = f"{timezone.now().year % 100:02d}user"

            derniers_ids = Utilisateur.objects.filter(
                user_id__startswith=prefix
            ).values_list("user_id", flat=True)

            numeros = [
                int(uid[-2:])
                for uid in derniers_ids
                if uid[-2:].isdigit()
            ]

            prochain = max(numeros, default=-1) + 1

            if prochain > 99:
                raise ValidationError(
                    "Le nombre maximal de 100 utilisateurs "
                    "est atteint pour cette année."
                )

            self.user_id = f"{prefix}{prochain:02d}"

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.role}"


class Entreprise(models.Model):
    raison_social = models.CharField(max_length=100)

    matricule_fiscal = models.CharField(
        max_length=20,
        unique=True,
        validators=[matricule_validator]
    )

    type_entreprise = models.CharField(
        max_length=15,
        choices=[
            ("chargeur", "Chargeur"),
            ("transporteur", "Transporteur"),
        ]
    )

    adresse = models.TextField(
        validators=[MinLengthValidator(
            20,
            "L'adresse doit contenir au moins 20 caractères."
        )]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    gerant = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="entreprise"
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.raison_social} - {self.matricule_fiscal}"
