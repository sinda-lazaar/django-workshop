
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Expedition(models.Model):
    reference = models.CharField(
        max_length=12,
        unique=True,
        editable=False
    )

    ville_depart = models.CharField(max_length=100)
    ville_arrive = models.CharField(max_length=100)

    date_souhaitee = models.DateField()

    poids_kg = models.DecimalField(
        max_digits=300,
        decimal_places=3,
        validators=[MinValueValidator(0.01)]
    )

    description = models.TextField()

    statut = models.CharField(
        max_length=20,
        choices=[
            ("publiee", "Publiée"),
            ("attribuee", "Attribuée"),
            ("en_cours", "En cours"),
            ("livree", "Livrée"),
            ("annulee", "Annulée"),
        ],
        default="publiee"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entreprise = models.ForeignKey(
        "EntreprisesApp.Entreprise",
        on_delete=models.CASCADE,
        related_name="expeditions"
    )

    def save(self, *args, **kwargs):
        if not self.reference:
            from django.utils import timezone

            prefix = f"EXP-{timezone.now().year % 100:02d}-"

            references = Expedition.objects.filter(
                reference__startswith=prefix
            ).values_list("reference", flat=True)

            numeros = [
                int(ref[-5:])
                for ref in references
                if ref[-5:].isdigit()
            ]

            prochain = max(numeros, default=0) + 1

            if prochain > 99999:
                raise ValidationError(
                    "Le compteur des expéditions est épuisé pour cette année."
                )

            self.reference = f"{prefix}{prochain:05d}"

        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        if self.entreprise_id:
            if self.entreprise.type_entreprise != "chargeur":
                raise ValidationError({
                    "entreprise": (
                        "Une expédition doit appartenir à une "
                        "entreprise de type chargeur."
                    )
                })

    def __str__(self):
        return (
            f"{self.reference} - "
            f"{self.ville_depart} → {self.ville_arrive}"
        )
