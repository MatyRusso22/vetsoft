from django.test import TestCase
from app.models import Client
from app.models import Provider
from app.models import Product,validate_product

class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": "221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555232")

class ProviderModelTest(TestCase):
    def test_can_create_and_get_provider(self):
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

    def test_can_update_provider(self):
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

    def test_update_provider_with_error(self):
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

class ProductModelTest(TestCase):

    def test_validate_product_price(self):
        data = {
            'name': 'Hueso',
            'type': 'Juguete',
            'price': -100
        }
        errors = validate_product(data)
        self.assertIn('price', errors)
        self.assertEqual(errors['price'], 'Por favor ingrese un precio del producto mayor que cero')

    def test_can_create_and_get_product(self):
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