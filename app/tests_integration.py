from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client
from app.models import Provider
from app.models import Pet
from datetime import date


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

class PetsTest(TestCase):
    def test_form_use_pet_form_template(self):
        response = self.client.get(reverse("pets_form"))
        self.assertTemplateUsed(response, "pets/form.html")

    def test_can_create_pets(self):
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Micho",
                "breed": "",
                "weight": 2,
                "birthday": "2024-04-04"
            },
        )
        pet = Pet.objects.all()
        self.assertEqual(len(pet), 1)

        self.assertEqual(pet[0].name, "Micho")
        self.assertEqual(pet[0].breed, "")
        self.assertEqual(pet[0].weight, 2)
        self.assertEqual(pet[0].birthday, date(2024, 4, 4))

        self.assertRedirects(response, reverse("pets_repo"))

    def test_should_response_with_404_status_if_pet_doesnt_exists(self):
        response = self.client.get(reverse("pets_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)
    
    def test_validation_weight_cant_be_cero(self):
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Tito",
                "breed": "",
                "weight": 0,
                "birthday": "2024-04-04"
            },
        ) 
        self.assertContains(response, "El peso debe ser mayor que 0")
    
    def test_validation_weight_cant_be_negative(self):
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Negro",
                "breed": "",
                "weight": -1,
                "birthday": "2024-04-04"
            },
        ) 
        self.assertContains(response, "El peso debe ser mayor que 0")
