from django.test import TestCase

from app.models import (
    Client,
    Medicine,
    Pet,
    Product,
    Provider,
    Vet,
    validate_medicine,
    validate_product,
    validate_Vet,
)


class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        """
        Prueba la creación de un cliente y la obtención del mismo.
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "54221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")

    def test_can_update_client(self):
        """
        Prueba la actualización de un cliente existente.
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "54221555232")

        client.update_client({"phone": "54221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "54221555233")

    def test_update_client_with_error(self):
        """
        Verifica que no se pueda actualizar un cliente con datos incorrectos.
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "54221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "54221555232")
    
    def test_validate_client_phone_invalid(self):
        """
        Verifica la validación de un telefono no numerico al guardar un cliente.
        """
        result, errors = Client.save_client({
            "name": "Telefono invalido",
            "phone": "letrasenvezdenumero",
            "address": "7 y 50",
            "email": "asdsadsad@vetsoft.com",
        })
        self.assertEqual(result, False)
        self.assertDictEqual(errors, {'phone': 'Por favor ingrese un telefono valido'})

    def test_validate_client_phone_valid(self):
        """
        Verifica la validación de un telefono de cliente válido.
        """
        data = {
            'name': 'Juan Sebastian Veron',
            'phone': '542213190689',
            'address': '13 y 44',
            'email': 'brujita75@vetsoft.com',
        }
        errors = validate_product(data)
        self.assertNotIn('client', errors)

class ProviderModelTest(TestCase):
    def test_can_create_and_get_provider_with_address(self):
        """
        Prueba la creación de un proveedor con dirección y la obtención del mismo.
        """
        Provider.save_provider(
            {
                "name": "Luis Fernando Flores",
                "email": "Fernanf100@gmail.com",
                "address": "ElSalvador 245",
            }
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Luis Fernando Flores")
        self.assertEqual(providers[0].email, "Fernanf100@gmail.com")
        self.assertEqual(providers[0].address, "ElSalvador 245")

    def test_can_update_provider_address(self):
        """
        Prueba la actualización de la dirección de un proveedor.
        """
        Provider.save_provider(
            {
                "name": "Luis Fernando Flores",
                "email": "Fernanf100@gmail.com",
                "address": "ElSalvador 245",
            }
        )
        provider = Provider.objects.get(pk=1)

        self.assertEqual(provider.address, "ElSalvador 245")

        provider.update_provider({"address": "SanMartin 212"})

        provider_updated = Provider.objects.get(pk=1)

        self.assertEqual(provider_updated.address, "SanMartin 212")

    def test_update_provider_address_with_error(self):
        """
        Verifica que no se pueda actualizar la dirección de un proveedor con datos incorrectos.
        """
        Provider.save_provider(
            {
                "name": "Luis Fernando Flores",
                "email": "Fernanf100@gmail.com",
                "address": "ElSalvador 245",
            }
        )
        provider = Provider.objects.get(pk=1)

        self.assertEqual(provider.address, "ElSalvador 245")

        provider.update_provider({"address": ""})

        provider_updated = Provider.objects.get(pk=1)

        self.assertEqual(provider_updated.address, "ElSalvador 245")



class MedicineModelTest(TestCase):
    def test_can_create_and_get_medicine_with_valid_dose(self):
        """
        Prueba la creación de un medicamento con dosis válida y la obtención del mismo.
        """
        Medicine.save_medicine(
            {
                "name": "Ibuprofeno",
                "descripcion": "Dolores de cabeza",
                "dosis": 2,
            }
        )
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "Ibuprofeno")
        self.assertEqual(medicines[0].descripcion, "Dolores de cabeza")
        self.assertEqual(medicines[0].dosis, 2)

    def test_validate_product_dosis(self):
        """
        Verifica la validación de la dosis de un medicamento.
        """
        data = {
            'name': 'Paracetamol',
            'descripcion': 'Dolores de cabeza',
            'dosis': -100
        }
        errors = validate_medicine(data)
        self.assertIn('dosis', errors)
        self.assertEqual(errors['dosis'], 'La dosis debe ser mayor a cero')


class ProductModelTest(TestCase):

    def test_validate_product_price(self):
        """
        Verifica la validación del precio de un producto negativo.
        """
        data = {
            'name': 'Hueso',
            'type': 'Juguete',
            'price': -100
        }
        errors = validate_product(data)
        self.assertIn('price', errors)
        self.assertEqual(errors['price'], 'Por favor ingrese un precio del producto mayor que cero')

    def test_validate_product_price_zero(self):
        """
        Verifica la validación del precio de un producto igual a cero.
        """
        data = {
            'name': 'Hueso',
            'type': 'Juguete',
            'price': 0
        }
        errors = validate_product(data)
        self.assertIn('price', errors)
        self.assertEqual(errors['price'], 'Por favor ingrese un precio del producto mayor que cero')

    def test_validate_product_price_non_numeric(self):
        """
        Verifica la validación del precio de un producto no numérico.
        """
        data = {
            'name': 'Hueso',
            'type': 'Juguete',
            'price': 'abc'
        }
        errors = validate_product(data)
        self.assertIn('price', errors)
        self.assertEqual(errors['price'], 'Por favor ingrese un precio valido para el producto')

    def test_validate_product_price_valid(self):
        """
        Verifica la validación de un precio de producto válido.
        """
        data = {
            'name': 'Hueso',
            'type': 'Juguete',
            'price': 100.0
        }
        errors = validate_product(data)
        self.assertNotIn('price', errors)

    def test_can_create_and_get_product(self):
        """
        Prueba la creación de un producto y la obtención del mismo.
        """
        Product.save_product(
            {
                "name": "Hueso",
                "type": "Juguete",
                "price": 100.0,
            }
        )
        products = Product.objects.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Hueso")
        self.assertEqual(products[0].type, "Juguete")
        self.assertEqual(products[0].price, 100.0)

    def test_can_update_product(self):
        """
        Prueba la actualización de un producto existente.
        """
        Product.save_product(
            {
                "name": "Hueso",
                "type": "Juguete",
                "price": 100.0,
            }
        )
        product = Product.objects.get(pk=1)
        self.assertEqual(product.price, 100.0)
        product.update_product( {
            'name': 'Hueso',
            'type': 'Juguete',
            'price': 200.0
           } )
        product_updated = Product.objects.get(pk=1)
        self.assertEqual(product_updated.price, 200.0)
        
    def test_validate_update_product_price_negative(self):
        """
        Verifica la validación del precio de un producto negativo al actualizarlo.
        """
        product = Product.save_product(
            {
                "name": "Hueso",
                "type": "Juguete",
                "price": 100.0,
            }
        )
        product = Product.objects.get(pk=1)
        ValueError,errors = product.update_product({
            'name': 'Hueso',
            'type': 'Juguete',
            'price': -200.0
        })
        self.assertIn('price', errors)
        self.assertEqual(errors['price'], 'Por favor ingrese un precio del producto mayor que cero')

    def test_validate_update_product_price_zero(self):
        """
        Verifica la validación del precio de un producto igual a cero al actualizarlo.
        """
        product = Product.save_product(
            {
                "name": "Hueso",
                "type": "Juguete",
                "price": 100.0,
            }
        )
        product = Product.objects.get(pk=1)
        ValueError,errors = product.update_product({
            'name': 'Hueso',
            'type': 'Juguete',
            'price': 0
        })
        self.assertIn('price', errors)
        self.assertEqual(errors['price'], 'Por favor ingrese un precio del producto mayor que cero')

class PetModelTest(TestCase):
    def test_invalid_weight(self):
        """
        Verifica la validación de un peso negativo al guardar una mascota.
        """
        result, errors = Pet.save_pet({
            "name": "Mascota Invalida",
            "breed": "no pasa",
            "weight": -5.0, #peso negativo, deberia no dejar guardar
            "birthday": "2024-02-11",
        })
        self.assertEqual(result, False)
        self.assertDictEqual(errors, {'weight': 'El peso debe ser mayor que 0'})

    def test_valid_weight(self):
        """ 
        Prueba la creación de una mascota con un peso válido. 
        """
        result, errors = Pet.save_pet({
            "name": "Mascota Valida",
            "breed": "pasa",
            "weight": 5.0, #peso valido, deberia guardarse la mascota
            "birthday": "2024-02-11",
        })
        self.assertEqual(result, True)
        self.assertIsNone(errors)


class VetModelTest(TestCase):
    def test_can_create_and_get_vet(self):
        """
        Valida la creacion de un veterinario y los datos
        """
        success, errors = Vet.save_vet(
            {
                "name": "Juan Perez",
                "email": "juan@example.com",
                "phone": "123456789",
                "speciality": "Cardiologia",  # Usa la especialidad correcta
            }
        )
        self.assertTrue(success)
        self.assertIsNone(errors)

        vets = Vet.objects.all()
        self.assertEqual(len(vets), 1)

        self.assertEqual(vets[0].name, "Juan Perez")
        self.assertEqual(vets[0].email, "juan@example.com")
        self.assertEqual(vets[0].phone, "123456789")
        self.assertEqual(vets[0].speciality, "Cardiologia")

    def test_validate_vet_speciality(self):
        """
        Valida el error a la creacion de un veterinario con una especialidad no valida
        """
        data = {
            'name': 'Juan Perez',
            'email': 'juan@example.com',
            'phone': '123456789',
            'speciality': 'oftalmologia'  # Una especialidad inválida
        }
        errors = validate_Vet(data)
        self.assertIn('speciality', errors)
        self.assertEqual(errors['speciality'], 'Especialidad no válida')

    def test_validate_vet_empty_speciality(self):
        """
        Valida el error a la creacion de un veterinario con una especialidad vacia
        """
        data = {
            'name': 'Juan Perez',
            'email': 'juan@example.com',
            'phone': '123456789',
            'speciality': ''  # Una especialidad vacia
        }
        errors = validate_Vet(data)
        self.assertIn('speciality', errors)
        self.assertEqual(errors['speciality'], 'Por favor seleccione una especialidad válida')

    def test_can_update_vet(self):
        """
        Prueba la actualización de un veterinario existente.
        """
        Vet.save_vet(
            {
                "name": "Juan Perez",
                "email": "juan@example.com",
                "phone": "123456789",
                "speciality": "Cardiologia",  
            }
        )
        vet = Vet.objects.get(pk=1)
        self.assertEqual(vet.speciality, 'Cardiologia')
        vet.update_vet( {
                "name": "Juan Perez",
                "email": "juan@example.com",
                "phone": "123456789",
                "speciality": "Clinica",  
            } )
        vet_updated = Vet.objects.get(pk=1)
        self.assertEqual(vet_updated.speciality, 'Clinica')        

      