from django.test import TestCase
from app.models import Client
from app.models import Pet
from datetime import datetime



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
class PetModelTest(TestCase):
    def test_update_pet_with_negative_weight(self):
        # Crear una mascota
        pet = Pet.objects.create(
            name="Roma",
            breed="",
            weight=25,
            birthday="2020-02-02",
        )

        # Intentar actualizar con un peso negativo
        success, errors = pet.update_pet({
            "name": "Roma",
            "breed": "",
            "weight": -30,  # Peso negativo
            "birthday": "2020-02-02",
        })

        # Debería fallar, así que success debería ser False
        self.assertFalse(success)

        # Verificar que el número de teléfono no haya cambiado
        self.assertEqual(pet.weight, 25)