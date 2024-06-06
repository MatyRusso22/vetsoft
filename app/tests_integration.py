from datetime import date

from django.shortcuts import reverse
from django.test import TestCase

from app.models import (
    Client,
    Medicine,
    Pet,
    Product,
    Provider,
    Vet,
    City
)


class HomePageTest(TestCase):
    
    def test_use_home_template(self):
        """
        Verifica que se use la plantilla de inicio. 
        """
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ClientsTest(TestCase):

    def test_repo_use_repo_template(self):
        """
        Verifica que se use la plantilla del repositorio de clientes. 
        """
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_repo_display_all_clients(self):
        """
        Verifica que se muestre la plantilla con todos los clientes. 
        """
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_form_use_form_template(self):
        """
        Verifica que se use la plantilla del formulario de clientes. 
        """
        response = self.client.get(reverse("clients_form"))
        self.assertTemplateUsed(response, "clients/form.html")

    def test_can_create_client(self):
        """
        Prueba la creación de un cliente y la redirección al repositorio de clientes. 
        """
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": 54221555232,
                "city": "La Plata",
                "email": "brujita75@vetsoft.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, 54221555232)
        self.assertEqual(clients[0].city, "La Plata")
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")

        self.assertRedirects(response, reverse("clients_repo"))

    def test_validation_errors_create_client(self):
        """
        Verifica los errores de validación al crear un cliente sin datos. 
        """
        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")

    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        """
        Verifica que se responda con el estado 404 si el cliente no existe. 
        """
        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        """
        Verifica la validación de un email inválido al crear un cliente. 
        """
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "city": "La Plata",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email válido")
    
    def test_validation_invalid_name(self):
        """
        Verifica la validación de un nombre inválido al crear un cliente. 
        """
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Ju4n Sebastian Veron",
                "phone": "54221555232",
                "city": "La Plata",
                "email": "brujita75@gmail.com",
            },
        )

        self.assertContains(response, "El nombre solo puede contener letras y espacios")

    def test_edit_user_with_valid_data(self):
        """
        Prueba la edición de un cliente con datos válidos y la redirección correcta. 
        """
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city="La Plata",
            phone=54221555232,
            email="brujita75@vetsoft.com",
        )

        response = self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Guido Carrillo",
                "city": "La Plata",
                "phone": 54221555232,
                "email": "brujita75@vetsoft.com",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.name, "Guido Carrillo")
        self.assertEqual(editedClient.phone, client.phone)
        self.assertEqual(editedClient.city, client.city)
        self.assertEqual(editedClient.email, client.email)
    
    def test_validation_invalid_phone(self):
        """
        Verifica la validación de un telefono inválido al crear un cliente. 
        """
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "asdhashdh",
                "city": "La Plata",
                "email": "brujita75@vetsoft.com",
            },
        )

        self.assertContains(response, "Por favor ingrese un telefono valido")

    def test_edit_user_with_invalid_data_test_city(self):
        """"
        Test para editar un cliente con datos validos y chequeo de ciudad
        """
        client = Client.objects.create(
            name="Pepe",
            city="La Plata",
            phone="54114587536",
            email="pep10@vetsoft.com",
        )


        self.client.post(
            reverse("clients_form"),
              data={
                "id": client.id,
                "name": "Pepe",
                "phone": "54114587536",
                "city": "Ciudad inexistente",
                "email": "pep10@vetsoft.com",
            },
        )

        # redirect after post
        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.city, "La Plata")

    def test_edit_user_with_invalid_data_test_email_not_end_vetsoft(self):
        """"
        Test para editar un cliente con datos validos y con email sin terminar en vetsoft
        """
        client = Client.objects.create(
            name="Pepe",
            city="La Plata",
            phone="54114587536",
            email="pep10@vetsoft.com",
        )


        self.client.post(
            reverse("clients_form"),
              data={
                "id": client.id,
                "name": "Pepe",
                "phone": "54114587536",
                "city": "La Plata",
                "email": "pep10@gmail.com",
            },
        )

        # redirect after post
        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.email, "pep10@vetsoft.com")

class ProvidersTest(TestCase):

    def test_can_create_provider_with_valid_address(self):
        """
        Prueba que se pueda crear un nuevo proveedor con una dirección válida.
        """
        
        response = self.client.post(
            reverse("provider_form"),
            data={
                "name": "Luis Fernando Flores",
                "email": "Fernanf100@gmail.com",
                "address": "Calle 13 y Calle 56",
            },
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Luis Fernando Flores")
        self.assertEqual(providers[0].email, "Fernanf100@gmail.com")
        self.assertEqual(providers[0].address, "Calle 13 y Calle 56")

        self.assertRedirects(response, reverse("provider_repo"))

    def test_validation_errors_create_provider_with_invalid_address(self):
        """
        Prueba que se muestren errores de validación si se proporciona una dirección inválida al crear un proveedor.
        """
        response = self.client.post(
            reverse("provider_form"),
            data={
                "name": "Luis Fernando Flores",
                "email": "Fernanf100@gmail.com",
                "address": "",  # Dirección vacía
            },
        )

        self.assertContains(response, "Por favor ingrese una dirección")

    def test_edit_provider_with_valid_address(self):  
        """
        Prueba que se pueda editar un proveedor existente con una dirección válida.
        """
        provider = Provider.objects.create(
            name="Luis Fernando Flores",
            address="Calle 13 y Calle 56",
            email="Fernanf100@gmail.com",
        )

        response = self.client.post(
            reverse("provider_form"),
            data={
                "id": provider.id,
                "name": "Carlos Tevez",
                "address": "Calle 14 y Calle 57",
            },
        )

        self.assertEqual(response.status_code, 302)

        editedProvider = Provider.objects.get(pk=provider.id)
        self.assertEqual(editedProvider.name, "Carlos Tevez")
        self.assertEqual(editedProvider.address, "Calle 14 y Calle 57")
        self.assertEqual(editedProvider.email, provider.email)

    def test_edit_provider_with_invalid_address(self):
        """
        Prueba que no se pueda editar un proveedor existente con una dirección inválida ,si no que se quedara con la dirección valida que tenía
        """  
        provider = Provider.objects.create(
            name="Luis Fernando Flores",
            address="Calle 13 y Calle 56",
            email="Fernanf100@gmail.com",
        )

        response = self.client.post(
        reverse("provider_form"),
            data={
                "id": provider.id,
                "address": "",  # Dirección vacía
            },
        )

        self.assertEqual(response.status_code, 302)  # Debería devolver un código 302, indicando una redirección


        editedProvider = Provider.objects.get(pk=provider.id)
        self.assertEqual(editedProvider.name, "Luis Fernando Flores")  # El nombre no debería cambiar
        self.assertEqual(editedProvider.address, "Calle 13 y Calle 56")  # La dirección no debería cambiar
        self.assertEqual(editedProvider.email, provider.email)  # El correo electrónico no debería cambiar

class MedicinesTest(TestCase):

    def test_form_use_medicine_form_template(self):
        """
        Verifica que se use la plantilla del formulario de medicinas. 
        """
        response = self.client.get(reverse("medicines_form"))
        self.assertTemplateUsed(response, "medicines/form.html")

    def test_can_create_medicine(self):
        """
        Prueba la creación de una medicina y la redirección al repositorio de medicinas. 
        """
        response = self.client.post(
            reverse("medicines_form"),
            data={
                "name": "Ibuprofeno",
                "descripcion": "Dolores de cabeza",
                "dosis": 2,
            },
        )
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "Ibuprofeno")
        self.assertEqual(medicines[0].descripcion, "Dolores de cabeza")
        self.assertEqual(medicines[0].dosis, 2)

        self.assertRedirects(response, reverse("medicines_repo"))

    def test_should_response_with_404_status_if_medicine_doesnt_exists(self):
        """
        Verifica que se responda con el estado 404 si la medicina no existe. 
        """
        response = self.client.get(reverse("medicines_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_dosis_greater_than_ten(self):
        """
        Verifica la validación de una dosis mayor a diez al crear una medicina. 
        """
        response = self.client.post(
            reverse("medicines_form"),
            data={
                "name": "Paracetamol",
                "descripcion": "Dolores de cabeza",
                "dosis": 11,
            },
        ) 
        self.assertContains(response, "La dosis debe ser menor que 10")
    
    def test_validation_dosis_smaller_than_one(self):
        """
        Verifica la validación de una dosis menor a uno al crear una medicina. 
        """
        response = self.client.post(
            reverse("medicines_form"),
            data={
                "name": "Paracetamol",
                "descripcion": "Dolores de cabeza",
                "dosis": 0,
            },
        ) 
        self.assertContains(response, "La dosis debe ser mayor a cero")

    

class PetsTest(TestCase):
    def test_form_use_pet_form_template(self):
        """
        Verifica que se use la plantilla del formulario de mascotas. 
        """
        response = self.client.get(reverse("pets_form"))
        self.assertTemplateUsed(response, "pets/form.html")

    def test_can_create_pets(self):
        """
        Prueba la creación de una mascota y la redirección al repositorio de mascotas.
        """
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
        """
        Verifica que se responda con el estado 404 si la mascota no existe.
        """
        response = self.client.get(reverse("pets_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)
    
    def test_validation_weight_cant_be_cero(self):
        """
        Verifica la validación de un peso igual a cero al crear una mascota.
        """
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
        """
        Verifica la validación de un peso negativo al crear una mascota.
        """
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

 
class ProductTest(TestCase):
 
    def test_form_use_form_template(self):
        """
        Verifica que se use la plantilla del formulario de productos.
        """
        response = self.client.get(reverse("products_form"))
        self.assertTemplateUsed(response, "products/form.html")

    def test_can_create_product(self):
        """
        Prueba la creación de un producto y la redirección al repositorio de productos. 
        """
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "Cepillo",
                "type": "Higiene",
                "price": 100.0,
            },
        )
        
        products = Product.objects.all() 
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Cepillo")
        self.assertEqual(products[0].type, "Higiene")
        self.assertEqual(products[0].price, 100.0)
        self.assertRedirects(response, reverse("products_repo"))

    def test_validation_errors_create_product(self):
        """
        Verifica los errores de validación al crear un producto sin datos.
        """
        response = self.client.post(
            reverse("products_form"),
            data={},
        )       
        
        self.assertContains(response, "Por favor ingrese un nombre para el producto") 
        self.assertContains(response, "Por favor ingrese el tipo del producto")  
        self.assertContains(response, "Por favor ingrese el precio del producto")

    
    def test_should_response_with_404_status_if_product_doesnt_exists(self):
        """
        Verifica que se responda con el estado 404 si el producto no existe.
        """
        response = self.client.get(reverse("products_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_price_greater_than_zero(self):
        """
        Verifica la validación de un precio mayor que cero al crear un producto.
        """
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "Shampoo",
                "type": "Higiene",
                "price": -10.0,
            },
        ) 
        self.assertContains(response, "Por favor ingrese un precio del producto mayor que cero")

    def test_validation_price_zero(self):
        """
        Verifica la validación de un precio igual a cero al crear un producto.
        """
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "Shampoo",
                "type": "Higiene",
                "price": 0,
            },
        ) 
        self.assertContains(response, "Por favor ingrese un precio del producto mayor que cero")

    def test_validation_price_non_numeric(self):
        """
        Verifica la validación de un precio no numérico al crear un producto.
        """
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "Shampoo",
                "type": "Higiene",
                "price": "abc",
            },
        ) 
        self.assertContains(response, "Por favor ingrese un precio valido para el producto")
 

    def test_edit_product_with_valid_data(self):
        """
        Prueba la edición de un producto con datos válidos y la redirección correcta.
        """
        product = Product.objects.create(
            name="Shampoo",
            type="Higiene",
            price=100.0,
        )
        response = self.client.post(
            reverse("products_form"),
            data={
                "id": product.id,
                "name": "Shampoo premium",
                "type": "Higiene",
                "price": 200.0,
            },
        ) 
        self.assertEqual(response.status_code, 302)
        edited_product = Product.objects.get(pk=product.id)
        self.assertEqual(edited_product.name, "Shampoo premium")
        self.assertEqual(edited_product.type, product.type)
        self.assertEqual(edited_product.price, 200.0)
        
    def test_validation_price_greater_than_zero_on_edit(self):
        """
        Verifica la validación de un precio mayor que cero al editar un producto.
        """
        product = Product.objects.create(
            name="Shampoo",
            type="Higiene",
            price=100.0,
        )
        response = self.client.post(
            reverse("products_edit", kwargs={"id": product.id}),
            data={
                "name": "Shampoo",
                "type": "Higiene",
                "price": -10.0,
            },
        )
        self.assertContains(response, "Por favor ingrese un precio del producto mayor que cero")

    def test_validation_price_zero_on_edit(self):
        """
        Verifica la validación de un precio igual a cero al editar un producto.
        """
        product = Product.objects.create(
            name="Shampoo",
            type="Higiene",
            price=100.0,
        )
        response = self.client.post(
            reverse("products_edit", kwargs={"id": product.id}),
            data={
                "name": "Shampoo",
                "type": "Higiene",
                "price": 0,
            },
        )
        self.assertContains(response, "Por favor ingrese un precio del producto mayor que cero")

class VetSpecialityIntegrationTest(TestCase):
    def test_form_use_form_template(self):
        """
        Verifica que se use la plantilla de veterinario
        """
        response = self.client.get(reverse("vet_form"))
        self.assertTemplateUsed(response, "vet/form.html")
    
    def test_can_create_vet_with_valid_speciality(self):
        """
        Prueba de crear un veterinario con una especialidad.
        """
        self.client.post(reverse('vet_form'), {
            'name': 'Juan Perez',
            'email': 'juan@example.com',
            'phone': '123456789',
            'speciality': 'Cardiologia'
        })

        # Verifica que se ha creado un veterinario
        vets = Vet.objects.all()
        self.assertEqual(len(vets), 1)

        # Verifica que los datos del veterinario son correctos
        self.assertEqual(vets[0].name, 'Juan Perez')
        self.assertEqual(vets[0].email, 'juan@example.com')
        self.assertEqual(vets[0].phone, '123456789')
        self.assertEqual(vets[0].speciality, 'Cardiologia')

    def test_cannot_create_vet_with_invalid_speciality(self):
        """
        Prueba el error de crear un veterinario con una especialidad inválida
        """
        response = self.client.post(reverse('vet_form'), {
            'name': 'Juan Perez',
            'email': 'juan@example.com',
            'phone': '123456789',
            'speciality': 'Oftalmologia'  # Especialidad inválida
        })
        self.assertContains(response, 'Especialidad no válida')

        vets = Vet.objects.all()
        self.assertEqual(len(vets), 0)  # Verificar que no se creó el veterinario



    
       