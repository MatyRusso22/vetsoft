from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client
from app.models import Provider
from app.models import Medicine


class HomePageTest(TestCase):
    def test_use_home_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ClientsTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_repo_display_all_clients(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("clients_form"))
        self.assertTemplateUsed(response, "clients/form.html")

    def test_can_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

        self.assertRedirects(response, reverse("clients_repo"))

    def test_validation_errors_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")

    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_edit_user_with_valid_data(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        response = self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Guido Carrillo",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.name, "Guido Carrillo")
        self.assertEqual(editedClient.phone, client.phone)
        self.assertEqual(editedClient.address, client.address)
        self.assertEqual(editedClient.email, client.email)



class ProvidersTest(TestCase):

    def test_form_use_provider_form_template(self):
        response = self.client.get(reverse("provider_form"))
        self.assertTemplateUsed(response, "provider/form.html")

    def test_can_create_provider(self):
        response = self.client.post(
            reverse("provider_form"),
            data={
                "name": "Luis Fernando Flores",
                "email": "Fernanf100@gmail.com",
                "address": "ElSalvador 245",
            },
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Luis Fernando Flores")
        self.assertEqual(providers[0].email, "Fernanf100@gmail.com")
        self.assertEqual(providers[0].address, "ElSalvador 245")

        self.assertRedirects(response, reverse("provider_repo"))

    def test_validation_errors_create_provider(self):
        response = self.client.post(
            reverse("provider_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese una dirección")

    def test_should_response_with_404_status_if_provider_doesnt_exists(self):
        response = self.client.get(reverse("provider_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("provider_form"),
            data={
                "name": "Luis Fernando Flores",
                "email": "Fernanf100",
                "address": "ElSalvador 245",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_edit_provider_with_valid_data(self):
        provider = Provider.objects.create(
            name="Luis Fernando Flores",
            address="ElSalvador 245",
            email="Fernanf100@gmail.com",
        )

        response = self.client.post(
            reverse("provider_form"),
            data={
                "id": provider.id,
                "name": "Carlos Tevez",
                "address": "San Martin 212",
            },
        )

        self.assertEqual(response.status_code, 302)

        editedProvider = Provider.objects.get(pk=provider.id)
        self.assertEqual(editedProvider.name, "Carlos Tevez")
        self.assertEqual(editedProvider.address, "San Martin 212")
        self.assertEqual(editedProvider.email, provider.email)

class MedicinesTest(TestCase):

    def test_form_use_medicine_form_template(self):
        response = self.client.get(reverse("medicines_form"))
        self.assertTemplateUsed(response, "medicines/form.html")

    def test_can_create_medicine(self):
        response = self.client.post(
            reverse("medicines_form"),
            data={
                "name": "Ibuprofeno",
                "descripcion": "Dolores de cabeza",
                "dosis": "2",
            },
        )
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "Ibuprofeno")
        self.assertEqual(medicines[0].descripcion, "Dolores de cabeza")
        self.assertEqual(medicines[0].dosis, "2")

        self.assertRedirects(response, reverse("medicines_repo"))

    def test_should_response_with_404_status_if_medicine_doesnt_exists(self):
        response = self.client.get(reverse("medicines_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_dosis(self):
        response = self.client.post(
            reverse("medicines_form"),
            data={
                "name": "Ibuprofeno",
                "descripcion": "Dolores de cabeza",
                "dosis": "11",
            },
        )

        self.assertEqual(response.status_code, 302)

    def test_edit_medicine_with_invalid_dosis(self):
        medicine = Medicine.objects.create(
            name="Ibuprofeno",
            descripcion="Dolores de cabeza",
            dosis="5",
        )

        response = self.client.post(
            reverse("medicines_form"),
            data={
                "id": medicine.id,
                "name": "Ibuprofeno",
                "descripcion":"Dolores de cabeza",
                "dosis": "15",
            },
        )

        self.assertEqual(response.status_code, 302)

        editedMedicine = Medicine.objects.get(pk=medicine.id)
        self.assertEqual(editedMedicine.name, "Ibuprofeno")
        self.assertEqual(editedMedicine.descripcion, "Dolores de cabeza")
        self.assertEqual(editedMedicine.dosis, "15")
