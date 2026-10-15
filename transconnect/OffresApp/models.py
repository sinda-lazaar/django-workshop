
from django.db import models, transaction
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Offre(models.Model):
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    date_proposition = models.DateField(auto_now_add=True)

    delai_jours = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    statut = models.CharField(
        max_length=20,
        choices=[
            ("proposee", "Proposée"),
            ("acceptee", "Acceptée"),
            ("refusee", "Refusée"),
            ("retiree", "Retirée"),
        ],
        default="proposee"
    )

    transporteur = models.ForeignKey(
        "EntreprisesApp.Entreprise",
        on_delete=models.CASCADE,
        related_name="offres"
    )

    expedition = models.ForeignKey(
        "ExpeditionsApp.Expedition",
        on_delete=models.CASCADE,
        related_name="offres"
    )

    vehicule = models.ForeignKey(
        "VehiculesApp.Vehicule",
        on_delete=models.CASCADE,
        related_name="offres"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["transporteur", "expedition"],
                condition=Q(statut="proposee"),
                name="unique_offre_proposee_transporteur_expedition"
            )
        ]

    def clean(self):
        super().clean()

        # Règle 1 : l'entreprise qui propose doit être un transporteur.
        if self.transporteur_id:
            if self.transporteur.type_entreprise != "transporteur":
                raise ValidationError({
                    "transporteur": (
                        "Seule une entreprise de type transporteur "
                        "peut proposer une offre."
                    )
                })

        # Règles 2, 3, 4, 6 et 7.
        if self.expedition_id:
            expedition = self.expedition

            # Règle 3 : une nouvelle offre exige une expédition publiée.
            if self._state.adding and expedition.statut != "publiee":
                raise ValidationError({
                    "expedition": (
                        "Une offre ne peut être créée que pour "
                        "une expédition publiée."
                    )
                })

            # Règle 4 : une seule offre proposée active
            # par transporteur pour une expédition.
            if self.transporteur_id and self.statut == "proposee":
                doublon = Offre.objects.filter(
                    transporteur_id=self.transporteur_id,
                    expedition_id=self.expedition_id,
                    statut="proposee"
                ).exclude(pk=self.pk)

                if doublon.exists():
                    raise ValidationError(
                        "Ce transporteur possède déjà une offre "
                        "proposée pour cette expédition."
                    )

            if self.vehicule_id and self.transporteur_id:
                vehicule = self.vehicule

                # Règle 2 : le véhicule doit appartenir au transporteur.
                if vehicule.entreprise_id != self.transporteur_id:
                    raise ValidationError({
                        "vehicule": (
                            "Le véhicule doit appartenir à "
                            "l'entreprise qui propose l'offre."
                        )
                    })

                # Règle 6 : un véhicule indisponible ne peut pas
                # être utilisé pour une nouvelle offre.
                if self._state.adding and not vehicule.disponible:
                    raise ValidationError({
                        "vehicule": (
                            "Ce véhicule n'est pas disponible."
                        )
                    })

                # Règle 7 : compatibilité indicative entre le type
                # de véhicule et le poids de l'expédition.
                poids = float(expedition.poids_kg)

                limites = {
                    "camionnette": (0, 1500),
                    "fourgon": (0, 3500),
                    "camion_porteur": (3500, 19000),
                    "semi_remorque": (19000, 26000),
                }

                type_vehicule = vehicule.type_vehicule
                minimum, maximum = limites[type_vehicule]

                if not (minimum < poids <= maximum):
                    raise ValidationError({
                        "vehicule": (
                            "Le type du véhicule n'est pas compatible "
                            "avec le poids de cette expédition."
                        )
                    })

                if vehicule.capacite_kg < poids:
                    raise ValidationError({
                        "vehicule": (
                            "La capacité du véhicule est insuffisante "
                            "pour cette expédition."
                        )
                    })

    def save(self, *args, **kwargs):
        with transaction.atomic():
            ancien_statut = None

            if self.pk:
                ancien_statut = (
                    Offre.objects.filter(pk=self.pk)
                    .values_list("statut", flat=True)
                    .first()
                )

            self.full_clean()
            super().save(*args, **kwargs)

            # Règle 5 : cascade lors de l'acceptation.
            if (
                self.statut == "acceptee"
                and ancien_statut != "acceptee"
            ):
                self.expedition.statut = "attribuee"
                self.expedition.save(
                    update_fields=["statut", "updated_at"]
                )

                Offre.objects.filter(
                    expedition_id=self.expedition_id,
                    statut="proposee"
                ).exclude(pk=self.pk).update(
                    statut="refusee"
                )

    def __str__(self):
        return (
            f"Offre {self.pk} - {self.prix} DT - {self.statut}"
        )
