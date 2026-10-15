
from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError

from EntreprisesApp.models import Utilisateur, Entreprise
from VehiculesApp.models import Vehicule
from ExpeditionsApp.models import Expedition
from OffresApp.models import Offre


class OffreBusinessRulesTests(TestCase):

    def setUp(self):
        # Users
        self.user_chargeur = Utilisateur.objects.create_user(
            username="chargeur_test",
            email="chargeur_test@gmail.com",
            password="Test12345!",
            telephone="11111111",
        )

        self.user_transporteur1 = Utilisateur.objects.create_user(
            username="transporteur1_test",
            email="transporteur1_test@gmail.com",
            password="Test12345!",
            telephone="22222222",
        )

        self.user_transporteur2 = Utilisateur.objects.create_user(
            username="transporteur2_test",
            email="transporteur2_test@gmail.com",
            password="Test12345!",
            telephone="33333333",
        )

        # Companies
        self.chargeur = Entreprise.objects.create(
            raison_social="Chargeur Test",
            matricule_fiscal="1234567AAM001",
            type_entreprise="chargeur",
            adresse="Adresse de test suffisamment longue",
            gerant=self.user_chargeur,
        )

        self.transporteur1 = Entreprise.objects.create(
            raison_social="Transporteur Test 1",
            matricule_fiscal="2345678AAM002",
            type_entreprise="transporteur",
            adresse="Adresse de test suffisamment longue",
            gerant=self.user_transporteur1,
        )

        self.transporteur2 = Entreprise.objects.create(
            raison_social="Transporteur Test 2",
            matricule_fiscal="3456789AAM003",
            type_entreprise="transporteur",
            adresse="Adresse de test suffisamment longue",
            gerant=self.user_transporteur2,
        )

        # Vehicles
        self.vehicule1 = Vehicule.objects.create(
            immatriculation="TEST000001",
            type_vehicule="camion_porteur",
            capacite_kg=10000,
            disponible=True,
            entreprise=self.transporteur1,
        )

        self.vehicule2 = Vehicule.objects.create(
            immatriculation="TEST000002",
            type_vehicule="camion_porteur",
            capacite_kg=10000,
            disponible=True,
            entreprise=self.transporteur2,
        )

        # Published expedition
        self.expedition = Expedition.objects.create(
            ville_depart="Tunis",
            ville_arrive="Sousse",
            date_souhaitee=date.today(),
            poids_kg=5000,
            description="Expedition de test",
            statut="publiee",
            entreprise=self.chargeur,
        )

    def test_1_only_transporters_can_propose(self):
        offre = Offre(
            prix=500,
            delai_jours=2,
            transporteur=self.chargeur,
            expedition=self.expedition,
            vehicule=self.vehicule1,
        )

        with self.assertRaises(ValidationError):
            offre.full_clean()

    def test_2_vehicle_must_belong_to_transporter(self):
        offre = Offre(
            prix=500,
            delai_jours=2,
            transporteur=self.transporteur1,
            expedition=self.expedition,
            vehicule=self.vehicule2,
        )

        with self.assertRaises(ValidationError):
            offre.full_clean()

    def test_3_expedition_must_be_published(self):
        self.expedition.statut = "attribuee"
        self.expedition.save()

        offre = Offre(
            prix=500,
            delai_jours=2,
            transporteur=self.transporteur1,
            expedition=self.expedition,
            vehicule=self.vehicule1,
        )

        with self.assertRaises(ValidationError):
            offre.full_clean()

    def test_4_no_duplicate_proposed_offers(self):
        Offre.objects.create(
            prix=500,
            delai_jours=2,
            transporteur=self.transporteur1,
            expedition=self.expedition,
            vehicule=self.vehicule1,
        )

        second_offre = Offre(
            prix=600,
            delai_jours=3,
            transporteur=self.transporteur1,
            expedition=self.expedition,
            vehicule=self.vehicule1,
        )

        with self.assertRaises(ValidationError):
            second_offre.full_clean()

    def test_5_acceptance_updates_expedition_and_other_offers(self):
        offre1 = Offre.objects.create(
            prix=500,
            delai_jours=2,
            transporteur=self.transporteur1,
            expedition=self.expedition,
            vehicule=self.vehicule1,
        )

        offre2 = Offre.objects.create(
            prix=600,
            delai_jours=3,
            transporteur=self.transporteur2,
            expedition=self.expedition,
            vehicule=self.vehicule2,
        )

        offre1.statut = "acceptee"
        offre1.save()

        self.expedition.refresh_from_db()
        offre2.refresh_from_db()

        self.assertEqual(self.expedition.statut, "attribuee")
        self.assertEqual(offre2.statut, "refusee")

    def test_6_unavailable_vehicle_is_rejected(self):
        self.vehicule1.disponible = False
        self.vehicule1.save()

        offre = Offre(
            prix=500,
            delai_jours=2,
            transporteur=self.transporteur1,
            expedition=self.expedition,
            vehicule=self.vehicule1,
        )

        with self.assertRaises(ValidationError):
            offre.full_clean()

    def test_7_vehicle_type_and_capacity_must_be_compatible(self):
        self.vehicule1.type_vehicule = "camionnette"
        self.vehicule1.capacite_kg = 1500
        self.vehicule1.save()

        offre = Offre(
            prix=500,
            delai_jours=2,
            transporteur=self.transporteur1,
            expedition=self.expedition,
            vehicule=self.vehicule1,
        )

        with self.assertRaises(ValidationError):
            offre.full_clean()
