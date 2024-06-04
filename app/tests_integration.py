from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client
from app.models import Provider
from app.models import Medicine
from app.models import Pet
from datetime import date
from app.models import Product
from app.models import Vet , EspecialidadVeterinario


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

    def test_can_create_provider_with_valid_address(self):
        # Prueba que se pueda crear un nuevo proveedor con una dirección válida.
        
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
        # Prueba que se muestren errores de validación si se proporciona una dirección inválida al crear un proveedor.
        
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
        # Prueba que se pueda editar un proveedor existente con una dirección válida.
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
        #Prueba que no se pueda editar un proveedor existente con una dirección inválida ,si no que se quedara con la dirección valida que tenía

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
        response = self.client.get(reverse("medicines_form"))
        self.assertTemplateUsed(response, "medicines/form.html")

    def test_can_create_medicine(self):
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
        response = self.client.get(reverse("medicines_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_dosis_greater_than_ten(self):
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

 
class ProductTest(TestCase):
 
    def test_form_use_form_template(self):
        response = self.client.get(reverse("products_form"))
        self.assertTemplateUsed(response, "products/form.html")

    def test_can_create_product(self):
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
        response = self.client.post(
            reverse("products_form"),
            data={},
        )       
        
        self.assertContains(response, "Por favor ingrese un nombre para el producto") 
        self.assertContains(response, "Por favor ingrese el tipo del producto")  
        self.assertContains(response, "Por favor ingrese el precio del producto")

    
    def test_should_response_with_404_status_if_product_doesnt_exists(self):
        response = self.client.get(reverse("products_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_price_greater_than_zero(self):
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
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "Shampoo",
                "type": "Higiene",
                "price": "abc",
            },
        ) 
        self.assertContains(response, "Por favor ingrese un precio valido para el producto")

    def test_should_response_with_404_status_if_product_doesnt_exists(self):
        response = self.client.get(reverse("products_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_edit_product_with_valid_data(self):
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


class VetTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("vet_repo"))
        self.assertTemplateUsed(response, "vet/repository.html")

    def test_repo_display_all_vet(self):
        response = self.client.get(reverse("vet_repo"))
        self.assertTemplateUsed(response, "vet/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("vet_form"))
        self.assertTemplateUsed(response, "vet/form.html")

    def test_can_create_vet(self):
        response = self.client.post(
            reverse("vet_form"),
            data={
                "name": "Juan",
                "email": "juan@example.com",
                "phone": "1234567890",
                "speciality": EspecialidadVeterinario.CIRUGIA,  # Use the actual value from the enum
            },
        )
        vets = Vet.objects.all()
        self.assertEqual(len(vets), 1)

        self.assertEqual(vets[0].name, "Juan")
        self.assertEqual(vets[0].email, "juan@example.com")
        self.assertEqual(vets[0].phone, "1234567890")
        self.assertEqual(vets[0].speciality, EspecialidadVeterinario.CIRUGIA)

        self.assertRedirects(response, reverse("vet_repo"))

    def test_validation_errors_create_vet(self):
        response = self.client.post(
            reverse("vet_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese una especialidad")

    def test_validation_invalid_email_vet(self):
        response = self.client.post(
            reverse("vet_form"),
            data={
                "name": "Juan",
                "email": "invalidemail",  # Un email inválido
                "phone": "1234567890",
                "speciality": EspecialidadVeterinario.CIRUGIA,
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    
       