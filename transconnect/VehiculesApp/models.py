
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Vehicule(models.Model):
    immatriculation = models.CharField(
        max_length=10,
        unique=True
    )

    type_vehicule = models.CharField(
        max_length=20,
        choices=[
            ("camionnette", "Camionnette"),
            ("camion_porteur", "Camion porteur"),
            ("semi_remorque", "Semi-remorque"),
            ("fourgon", "Fourgon"),
        ]
    )

    capacite_kg = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    disponible = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entreprise = models.ForeignKey(
        "EntreprisesApp.Entreprise",
        on_delete=models.CASCADE,
        related_name="vehicules"
    )

    def clean(self):
        super().clean()

        if self.entreprise_id:
            if self.entreprise.type_entreprise != "transporteur":
                raise ValidationError({
                    "entreprise": (
                        "Un véhicule doit appartenir à une "
                        "entreprise de type transporteur."
                    )
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.immatriculation} - {self.type_vehicule}"
