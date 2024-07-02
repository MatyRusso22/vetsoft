import os
from datetime import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import Browser, expect, sync_playwright

from app.models import Client, Medicine, Pet, Product, Provider, Vet, City

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 1) == 1
slow_mo = os.environ.get("SLOW_MO", 0)


class PlaywrightTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        """
        Configuración inicial de la clase de prueba, lanza el navegador
        """
        super().setUpClass()
        cls.browser: Browser = playwright.chromium.launch(
            headless=headless, slow_mo=int(slow_mo)
        )

    @classmethod
    def tearDownClass(cls):
        """
        Finaliza y cierra el navegador al terminar todas las pruebas
        """
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        """
        Configuración inicial para cada prueba, abre una nueva página
        """
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        """Finaliza y cierra la página al terminar cada prueba"""
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    def test_should_have_navbar_with_links(self):
        """Prueba que el navbar tenga los enlaces correctos y visibles"""
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
        """Prueba que las tarjetas de inicio tengan los enlaces correctos y visibles"""
        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        """Prueba que muestra un mensaje si la tabla de clientes está vacía"""
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")
        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        """Prueba que muestra los datos de los clientes correctamente"""
        Client.objects.create(
            name="Juan Sebastián Veron",
            city="La Plata",
            phone=54221555232,
            email="brujita75@vetsoft.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            city="Ensenada",
            phone=54221232555,
            email="goleador@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()
        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("La Plata")).to_be_visible()
        expect(self.page.get_by_text("54221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("Ensenada")).to_be_visible()
        expect(self.page.get_by_text("54221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@vetsoft.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        """Prueba que muestra la acción de agregar un nuevo cliente"""
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        """Prueba que muestra la acción de editar un cliente"""
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city="La Plata",
            phone=54221555232,
            email="brujita75@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute("href", reverse("clients_edit", kwargs={"id": client.id}))

    def test_should_show_client_delete_action(self):
        """Prueba que muestra la acción de eliminar un cliente"""
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city="La Plata",
            phone=54221555232,
            email="brujita75@vetsoft.com",
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
        """Prueba que permite eliminar un cliente"""
        Client.objects.create(
            name="Juan Sebastián Veron",
            city="La Plata",
            phone=54221555232,
            email="brujita75@vetsoft.com",
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
        """Prueba que permite crear un nuevo cliente"""
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("La Plata")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("54221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).to_be_visible()
        expect(self.page.get_by_text("La Plata")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        """Prueba que muestra errores si el formulario es inválido"""
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Ciudad").select_option("La Plata")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email válido")).to_be_visible()

    def test_should_be_able_to_edit_a_client(self):
        """Prueba que permite editar un cliente existente"""
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city="La Plata",
            phone=54221555232,
            email="brujita75@vetsoft.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("54221232555")
        self.page.get_by_label("Email").fill("goleador@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("Ensenada")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("La Plata")).not_to_be_visible()
        expect(self.page.get_by_text("54221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("Ensenada")).to_be_visible()
        expect(self.page.get_by_text("54221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@vetsoft.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )
    def test_shouldnt_be_able_to_create_client_with_no_numeric_phone(self):
        """Prueba que no se pueda crear un cliente con un telefono no numerico"""
        with self.assertRaises(ValueError):
            client = Client.objects.create(
                name="Juan Sebastián Veron",
                city="La Plata",
                phone="nonumerico",
                email="brujita75@vetsoft.com",
            )

            self.assertEqual(Client.objects.count(), 0)
    
 

    def test_shouldnt_be_able_to_create_client_with_no_start_54_phone(self):
        """Prueba que no se pueda crear un cliente con un telefono que no empieza con 54"""
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}") 

        expect(self.page.get_by_role("form")).to_be_visible() 

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("La Plata")

        self.page.get_by_role("button", name="Guardar").click() 

        expect(self.page.get_by_text("El teléfono debe comenzar con 54")).to_be_visible() 

    def test_shouldnt_be_able_to_create_client_with_name_invalid(self):
        """Prueba que no se pueda crear un cliente con un nombre invalido"""
            
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}") 

        expect(self.page.get_by_role("form")).to_be_visible() 

        self.page.get_by_label("Nombre").fill("1111111")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("La Plata")
        self.page.get_by_role("button", name="Guardar").click() 

        expect(self.page.get_by_text("El nombre solo puede contener letras y espacios")).to_be_visible()

    def test_shouldnt_be_able_to_create_client_with_city_invalid(self):
        """Prueba que no se pueda crear un cliente con una ciudad invalida"""
            
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}") 

        expect(self.page.get_by_role("form")).to_be_visible() 

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")

        self.page.get_by_role("button", name="Guardar").click() 

        expect(self.page.get_by_text("Por favor ingrese una ciudad")).to_be_visible()

    def test_shouldnt_be_able_to_create_client_with_no_email_end_vetsoft(self):
        """Prueba que no se pueda crear un cliente con un email que no termina en @vetsoft"""
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}") 

        expect(self.page.get_by_role("form")).to_be_visible() 

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@gmail.com")
        self.page.get_by_label("Ciudad").select_option("La Plata")
        self.page.get_by_role("button", name="Guardar").click() 

        expect(self.page.get_by_text("El email debe terminar en @vetsoft.com")).to_be_visible() 

class ProvidersTestCase(PlaywrightTestCase):
    def test_should_show_providers_data(self):
        """Prueba que los datos de los proveedores se muestren en la página."""
        Provider.objects.create(
            name="Proveedor 1",
            address="Calle 7 # 1234",
            email="proveedor1@gmail.com",
        )

        Provider.objects.create(
            name="Proveedor 2",
            address="Calle 54 # 456",
            email="proveedor2@gmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).not_to_be_visible()

        expect(self.page.get_by_text("Proveedor 1")).to_be_visible()
        expect(self.page.get_by_text("Calle 7 # 1234")).to_be_visible()
        expect(self.page.get_by_text("proveedor1@gmail.com")).to_be_visible()

        expect(self.page.get_by_text("Proveedor 2")).to_be_visible()
        expect(self.page.get_by_text("Calle 54 # 456")).to_be_visible()
        expect(self.page.get_by_text("proveedor2@gmail.com")).to_be_visible()

    def test_should_show_add_provider_action(self):
        """Prueba que la acción 'Agregar Proveedor' se muestre en la página."""
        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        add_provider_action = self.page.get_by_role(
            "link", name="Nuevo proveedor", exact=False
        )
        expect(add_provider_action).to_have_attribute("href", reverse("provider_form"))

    def test_should_show_provider_address(self):
        """Prueba que la dirección del proveedor se muestre en la página."""
        Provider.objects.create(
            name="Proveedor con Dirección",
            address="Avenida 44 # 987",
            email="proveedor3@gmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        expect(self.page.get_by_text("Proveedor con Dirección")).to_be_visible()
        expect(self.page.get_by_text("Avenida 44 # 987")).to_be_visible()

    def test_should_be_able_to_create_provider_with_address(self):
        """Prueba que se pueda crear un proveedor con una dirección."""
        self.page.goto(f"{self.live_server_url}{reverse('provider_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Lucas")
        self.page.get_by_label("Dirección").fill("Calle 10 # 567")
        self.page.get_by_label("Email").fill("nuevoproveedor@gmail.com")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Lucas")).to_be_visible()
        expect(self.page.get_by_text("Calle 10 # 567")).to_be_visible()

    def test_should_view_error_if_address_is_not_provided_when_creating_provider(self):
        """Prueba que se muestre un error si no se proporciona una dirección al crear un proveedor."""
        self.page.goto(f"{self.live_server_url}{reverse('provider_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Nuevo Proveedor")
        self.page.get_by_label("Email").fill("nuevoproveedor@gmail.com")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dirección")).to_be_visible()

class MedicinesTestCase(PlaywrightTestCase):
    def test_should_show_medicines_data(self): 
        """Prueba que los datos de los medicamentos se muestren en la página."""
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
        """Prueba que la acción 'Agregar Medicamento' se muestre en la página."""
        self.page.goto(f"{self.live_server_url}{reverse('medicines_repo')}")

        add_medicine_action = self.page.get_by_role(
            "link", name="Nuevo medicamento", exact=False
        )
        expect(add_medicine_action).to_have_attribute("href", reverse("medicines_form"))
    

    def test_should_can_be_able_to_delete_a_medicine(self):
        """Prueba que se pueda eliminar un medicamento."""
        Medicine.objects.create(
            name="Buscapina",
            descripcion="Dolor de panza",
            dosis="5",
        )

        self.page.goto(f"{self.live_server_url}{reverse('medicines_repo')}")

        expect(self.page.get_by_text("Buscapina")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        """Prueba que se muestren errores si el formulario es inválido."""
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre para el medicamento")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una descripcion")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dosis")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Paracetamol")
        self.page.get_by_label("Descripcion").fill("Dolor de cabeza")
        self.page.get_by_label("Dosis").fill("-10")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("La dosis debe ser mayor a cero")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Ibuprofeno")
        self.page.get_by_label("Descripcion").fill("Dolor de cabeza")
        self.page.get_by_label("Dosis").fill("15")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("La dosis debe ser menor que 10")).to_be_visible()

class ProductTestCase(PlaywrightTestCase):
     def test_should_show_message_if_table_is_empty(self):
        """Prueba que se muestre un mensaje si la tabla está vacía."""
        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        expect(self.page.get_by_text("No existen productos")).to_be_visible()

     def test_should_show_products_data(self):
        """Prueba que se muestren los datos de los productos."""
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
        """Prueba que se muestre la acción 'Agregar Producto'."""
        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        add_product_action = self.page.get_by_role("link", name="Nuevo producto", exact=False)
        expect(add_product_action).to_have_attribute("href", reverse("products_form"))

     def test_should_show_product_edit_action(self):
        """Prueba que se muestre la acción de editar un producto."""
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
        """Prueba que se muestre la acción de eliminar un producto."""
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

      
     def test_should_view_errors_if_form_is_empty(self):
        """Prueba que se muestren errores si el formulario está vacío al crear un producto."""
        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Por favor ingrese un nombre para el producto")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese el tipo del producto")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese el precio del producto")).to_be_visible()

     def test_should_view_error_if_price_is_negative_on_create(self):
        """Prueba que se muestren errores si el precio es negativo al crear un producto."""
        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")
        self.page.get_by_label("Nombre").fill("Hueso")
        self.page.get_by_label("Tipo").fill("Juguete")
        self.page.get_by_label("Precio").fill("-10.0")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Por favor ingrese un precio del producto mayor que cero")).to_be_visible()

     def test_should_view_error_if_price_is_zero_on_create(self):
        """Prueba que se muestren errores si el precio es cero al crear un producto."""
        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")
        self.page.get_by_label("Nombre").fill("Hueso")
        self.page.get_by_label("Tipo").fill("Juguete")
        self.page.get_by_label("Precio").fill("0")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Por favor ingrese un precio del producto mayor que cero")).to_be_visible()
 
     def test_should_be_able_to_edit_a_product(self):
        """Prueba que se pueda editar un producto."""
        product = Product.objects.create(
            name="Hueso",
            type="Juguete",
            price=100.0,
        )
        path = reverse("products_edit", kwargs={"id": product.id})
        self.page.goto(f"{self.live_server_url}{path}")
        self.page.get_by_label("Nombre").fill("Hueso")
        self.page.get_by_label("Tipo").fill("Juguete")
        self.page.get_by_label("Precio").fill("200.0")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("200.0")).to_be_visible()

     def test_should_view_error_if_price_is_negative_on_edit(self):
        """Prueba que se muestren errores si el precio es negativo al editar un producto."""
        product = Product.objects.create(
            name="Hueso",
            type="Juguete",
            price=100.0,
        )
        path = reverse("products_edit", kwargs={"id": product.id})
        self.page.goto(f"{self.live_server_url}{path}")
        self.page.get_by_label("Nombre").fill("Hueso")
        self.page.get_by_label("Tipo").fill("Juguete")
        self.page.get_by_label("Precio").fill("-10.0")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Por favor ingrese un precio del producto mayor que cero")).to_be_visible()

     def test_should_view_error_if_price_is_zero_on_edit(self):
        """Prueba que se muestren errores si el precio es cero al editar un producto."""
        product = Product.objects.create(
            name="Hueso",
            type="Juguete",
            price=100.0,
        )
        path = reverse("products_edit", kwargs={"id": product.id})
        self.page.goto(f"{self.live_server_url}{path}")
        self.page.get_by_label("Nombre").fill("Hueso")
        self.page.get_by_label("Tipo").fill("Juguete")
        self.page.get_by_label("Precio").fill("0")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Por favor ingrese un precio del producto mayor que cero")).to_be_visible()

     def test_should_view_errors_if_edit_form_is_empty(self):
        """Prueba que se muestren errores si el formulario está vacío al editar un producto."""
        product = Product.objects.create(
            name="Hueso",
            type="Juguete",
            price=100.0,
        )
        path = reverse("products_edit", kwargs={"id": product.id})
        self.page.goto(f"{self.live_server_url}{path}")
        self.page.get_by_label("Nombre").fill("")
        self.page.get_by_label("Tipo").fill("")
        self.page.get_by_label("Precio").fill("")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Por favor ingrese un nombre para el producto")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese el tipo del producto")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese el precio del producto")).to_be_visible()

class PetsRepoTestCase(PlaywrightTestCase):
    def test_should_show_clients_data(self):
        """Prueba que se muestren los datos de las mascotas."""
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
        """Prueba que se muestre la acción de edición de una mascota."""
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
        """Prueba que se pueda eliminar una mascota."""
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

class VetSpecialityTestCase(PlaywrightTestCase):
  
    def test_should_be_able_to_create_vet_with_speciality(self):
        """
        Prueba que se pueda crear un veterinario con una especialidad.
        """
        self.page.goto(f"{self.live_server_url}{reverse('vet_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Dr. House")
        self.page.get_by_label("Email").fill("dr.house@example.com")
        self.page.get_by_label("Teléfono").fill("123456789")
        self.page.get_by_label("Especialidad").select_option("Clinica")

        self.page.get_by_role("button", name="Guardar").click()

        self.page.goto(f"{self.live_server_url}{reverse('vet_repo')}")

        expect(self.page.get_by_text("Dr. House")).to_be_visible()
        expect(self.page.get_by_text("Clinica")).to_be_visible()

    def test_should_be_able_to_edit_a_vet(self):
        """"
        Verifica la edicion de un veterinario
        """
        vet = Vet.objects.create(
            name="pepe",
            phone="1545789678",
            email="pep10@gmail.com",
            speciality = Vet.SPECIALITY_CHOICES.NEUROLOGIA,
        )

        self.page.goto(f"{self.live_server_url}{reverse('vet_edit', kwargs={'id': vet.id})}")

        self.page.get_by_label("Nombre").fill("messi")
        self.page.get_by_label("Teléfono").fill("1534998955")
        self.page.get_by_label("Email").fill("mess10@gmail.com")
        self.page.get_by_label("Especialidad").select_option("Cardiologia")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("pepe")).not_to_be_visible()
        expect(self.page.get_by_text("1545789678")).not_to_be_visible()
        expect(self.page.get_by_text("pep10@gmail.com")).not_to_be_visible()
        expect(self.page.get_by_text("Neurologia")).not_to_be_visible()

        expect(self.page.get_by_text("messi")).to_be_visible()
        expect(self.page.get_by_text("1534998955")).to_be_visible()
        expect(self.page.get_by_text("mess10@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("Cardiologia")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("vet_edit", kwargs={"id": vet.id}),
        )