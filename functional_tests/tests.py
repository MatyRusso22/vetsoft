import os
from datetime import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect, Browser

from django.urls import reverse

from app.models import Client

from app.models import Provider
from app.models import Pet
from app.models import Product

from app.models import Vet , EspecialidadVeterinario

from app.models import Medicine

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 1) == 1
slow_mo = os.environ.get("SLOW_MO", 0)


class PlaywrightTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser: Browser = playwright.chromium.launch(
            headless=headless, slow_mo=int(slow_mo)
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    def test_should_have_navbar_with_links(self):
        self.page.goto(self.live_server_url)

        navbar_home_link = self.page.get_by_test_id("navbar-Home")

        expect(navbar_home_link).to_be_visible()
        expect(navbar_home_link).to_have_text("Home")
        expect(navbar_home_link).to_have_attribute("href", reverse("home"))

        navbar_clients_link = self.page.get_by_test_id("navbar-Clientes")

        expect(navbar_clients_link).to_be_visible()
        expect(navbar_clients_link).to_have_text("Clientes")
        expect(navbar_clients_link).to_have_attribute("href", reverse("clients_repo"))

    def test_should_have_home_cards_with_links(self):
        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")
        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="221232555",
            email="goleador@gmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()
        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute("href", reverse("clients_edit", kwargs={"id": client.id}))

    def test_should_show_client_delete_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente"
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("clients_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class ClientCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_client(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email valido")).to_be_visible()

    def test_should_be_able_to_edit_a_client(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("221232555")
        self.page.get_by_label("Email").fill("goleador@gmail.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 44")).not_to_be_visible()
        expect(self.page.get_by_text("221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )

class ProvidersTestCase(PlaywrightTestCase):
    def test_should_show_providers_data(self):
        Provider.objects.create(
            name="Provider 1",
            address="123 Main St",
            email="provider1@example.com",
        )

        Provider.objects.create(
            name="Provider 2",
            address="456 Elm St",
            email="provider2@example.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).not_to_be_visible()

        expect(self.page.get_by_text("Provider 1")).to_be_visible()
        expect(self.page.get_by_text("123 Main St")).to_be_visible()
        expect(self.page.get_by_text("provider1@example.com")).to_be_visible()

        expect(self.page.get_by_text("Provider 2")).to_be_visible()
        expect(self.page.get_by_text("456 Elm St")).to_be_visible()
        expect(self.page.get_by_text("provider2@example.com")).to_be_visible()

    def test_should_show_add_provider_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        add_provider_action = self.page.get_by_role(
            "link", name="Nuevo proveedor", exact=False
        )
        expect(add_provider_action).to_have_attribute("href", reverse("provider_form"))

class VetTestCase(PlaywrightTestCase):
    def test_should_show_vet_edit_action(self):
        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="221555232",
            speciality="EspecialidadVeterinario.CIRUGIA",
        )

        self.page.goto(f"{self.live_server_url}{reverse('vet_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute("href", reverse("vet_edit", kwargs={"id": vet.id}))


class MedicinesTestCase(PlaywrightTestCase):
    def test_should_show_medicines_data(self):
        Medicine.objects.create(
            name="Ibuprofeno",
            descripcion="Dolores de cabeza",
            dosis=5,
        )

        Medicine.objects.create(
            name="Buscapina",
            descripcion="Dolores de estomago",
            dosis=10,
        )

        self.page.goto(f"{self.live_server_url}{reverse('medicines_repo')}")

        expect(self.page.get_by_text("No existen medicamentos")).not_to_be_visible()

        expect(self.page.get_by_text("Ibuprofeno")).to_be_visible()
        expect(self.page.get_by_text("Dolores de cabeza")).to_be_visible()
        expect(self.page.get_by_text("5")).to_be_visible()

        expect(self.page.get_by_text("Buscapina")).to_be_visible()
        expect(self.page.get_by_text("Dolores de estomago")).to_be_visible()
        expect(self.page.get_by_text("10")).to_be_visible()

    def test_should_show_add_medicine_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_repo')}")

        add_medicine_action = self.page.get_by_role(
            "link", name="Nuevo medicamento", exact=False
        )
        expect(add_medicine_action).to_have_attribute("href", reverse("medicines_form"))
    

    def test_should_can_be_able_to_delete_a_medicine(self):
        Medicine.objects.create(
            name="Buscapina",
            descripcion="Dolor de panza",
            dosis="5",
        )

        self.page.goto(f"{self.live_server_url}{reverse('medicines_repo')}")

        expect(self.page.get_by_text("Buscapina")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre para el medicamento")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una descripcion")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dosis")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Paracetamol")
        self.page.get_by_label("Descripcion").fill("Dolor de cabeza")
        self.page.get_by_label("Dosis").fill("-10.0")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("La dosis debe ser mayor a cero")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Ibuprofeno")
        self.page.get_by_label("Descripcion").fill("Dolor de cabeza")
        self.page.get_by_label("Dosis").fill("15")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("La dosis debe ser menor que 10")).to_be_visible()

class ProductsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        expect(self.page.get_by_text("No existen productos")).to_be_visible()

    def test_should_show_products_data(self):
        Product.objects.create(
            name="Peine",
            type="Higiene",
            price=100.0,
        )

        Product.objects.create(
            name="Pelota",
            type="Juguete",
            price=150.0,
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        expect(self.page.get_by_text("No existen productos")).not_to_be_visible() 
        expect(self.page.get_by_text("Peine")).to_be_visible()
        expect(self.page.get_by_text("Higiene")).to_be_visible()
        expect(self.page.get_by_text("100.0")).to_be_visible()

        expect(self.page.get_by_text("Pelota")).to_be_visible()
        expect(self.page.get_by_text("Juguete")).to_be_visible()
        expect(self.page.get_by_text("150.0")).to_be_visible()

    def test_should_show_add_product_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        add_product_action = self.page.get_by_role("link", name="Nuevo producto", exact=False)
        expect(add_product_action).to_have_attribute("href", reverse("products_form"))

    def test_should_show_product_edit_action(self):
        product = Product.objects.create(
            name="Peine",
            type="Higiene",
            price=100.0,
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("products_edit", kwargs={"id": product.id})
        )

    def test_should_show_product_delete_action(self):
        product = Product.objects.create(
            name="Peine",
            type="Higiene",
            price=100.0,
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        delete_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de producto"
        )
        product_id_input = delete_form.locator("input[name=product_id]")

        expect(delete_form).to_be_visible()
        expect(delete_form).to_have_attribute("action", reverse("products_delete"))
        expect(product_id_input).not_to_be_visible()
        expect(product_id_input).to_have_value(str(product.id))
        expect(delete_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_be_able_to_delete_a_product(self):
        Product.objects.create(
            name="Peine",
            type="Higiene",
            price="100.0",
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        expect(self.page.get_by_text("Peine")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("products_delete")) != -1

        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Peine")).not_to_be_visible()


class ProductCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_product(self):
        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Peine")
        self.page.get_by_label("Tipo").fill("Higiene")
        self.page.get_by_label("Precio").fill("100.0")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Peine")).to_be_visible()
        expect(self.page.get_by_text("Higiene")).to_be_visible()
        expect(self.page.get_by_text("100.0")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre para el producto")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese el tipo del producto")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese el precio del producto")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Peine")
        self.page.get_by_label("Tipo").fill("Higiene")
        self.page.get_by_label("Precio").fill("-10.0")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un precio del producto mayor que cero")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Peine")
        self.page.get_by_label("Tipo").fill("Higiene")
        self.page.get_by_label("Precio").fill("0")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un precio del producto mayor que cero")).to_be_visible()

    def test_should_be_able_to_edit_a_product(self):
        product = Product.objects.create(
            name="Peine",
            type="Higiene",
            price=100.0,
        )

        path = reverse("products_edit", kwargs={"id": product.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Pelota")
        self.page.get_by_label("Tipo").fill("Juguete")
        self.page.get_by_label("Precio").fill("150.0")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Peine")).not_to_be_visible()
        expect(self.page.get_by_text("Higiene")).not_to_be_visible()
        expect(self.page.get_by_text("100.0")).not_to_be_visible()

        expect(self.page.get_by_text("Pelota")).to_be_visible()
        expect(self.page.get_by_text("Juguete")).to_be_visible()
        expect(self.page.get_by_text("150.0")).to_be_visible()

    def test_should_view_errors_if_edit_form_is_invalid(self):
        product = Product.objects.create(
            name="Peine",
            type="Higiene",
            price=100.0,
        )

        path = reverse("products_edit", kwargs={"id": product.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Pelota")
        self.page.get_by_label("Tipo").fill("Juguete")
        self.page.get_by_label("Precio").fill("150.0")

        self.page.get_by_label("Nombre").fill("Peine")
        self.page.get_by_label("Tipo").fill("Higiene")
        self.page.get_by_label("Precio").fill("-10.0")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un precio del producto mayor que cero")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Peine")
        self.page.get_by_label("Tipo").fill("Higiene")
        self.page.get_by_label("Precio").fill("0")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un precio del producto mayor que cero")).to_be_visible()


class ProvidersTestCase(PlaywrightTestCase):
    def test_should_show_providers_data(self):
        Provider.objects.create(
            name="Provider 1",
            address="123 Main St",
            email="provider1@example.com",
        )

        Provider.objects.create(
            name="Provider 2",
            address="456 Elm St",
            email="provider2@example.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).not_to_be_visible()

        expect(self.page.get_by_text("Provider 1")).to_be_visible()
        expect(self.page.get_by_text("123 Main St")).to_be_visible()
        expect(self.page.get_by_text("provider1@example.com")).to_be_visible()

        expect(self.page.get_by_text("Provider 2")).to_be_visible()
        expect(self.page.get_by_text("456 Elm St")).to_be_visible()
        expect(self.page.get_by_text("provider2@example.com")).to_be_visible()

    def test_should_show_add_provider_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        add_provider_action = self.page.get_by_role(
            "link", name="Nuevo proveedor", exact=False
        )
        expect(add_provider_action).to_have_attribute("href", reverse("provider_form"))

class PetsRepoTestCase(PlaywrightTestCase):
    def test_should_show_clients_data(self):
        Pet.objects.create(
            name="Roma",
            breed="Labrador",
            weight="20",
            birthday="2018-02-11",
        )
        Pet.objects.create(
            name="Toto",
            breed="Schnauzer",
            weight="15",
            birthday="2008-05-05",
        )

        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")

    def test_should_show_pet_edit_action(self):
        pet_instance = Pet.objects.create(
            name="Roma",
            breed="Labrador",
            weight="20",
            birthday=datetime.strptime("11-02-2018", "%d-%m-%Y").strftime("%Y-%m-%d"),
        )

        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("pets_edit", kwargs={"id": pet_instance.id})
        )


    def test_should_can_be_able_to_delete_a_pet(self):
        Pet.objects.create(
            name="Lola",
            breed="",
            weight="22",
            birthday="2019-08-08",
        )

        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")

        expect(self.page.get_by_text("Lola")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("pets_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Lola")).not_to_be_visible()
