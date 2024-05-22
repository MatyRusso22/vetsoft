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
    def test_can_create_and_get_pet(self):
        success, errors = Pet.save_pet(
            {
                "name": "Toto",
                "breed": "Labrador",
                "weight": 25.0,
                "birthday": "01-05-2018",
            }
        )
        self.assertTrue(success)
        self.assertIsNone(errors)

        pets = Pet.objects.all()
        self.assertEqual(len(pets), 1)

        self.assertEqual(pets[0].name, "Toto")
        self.assertEqual(pets[0].breed, "Labrador")
        self.assertEqual(pets[0].weight, 25.0)
        self.assertEqual(pets[0].birthday.strftime("%d-%m-%Y"), "01-05-2018")

    def test_can_update_pet(self):
        success, errors = Pet.save_pet(
            {
                "name": "Roma",
                "breed": "",
                "weight": 25.0,
                "birthday": "11-02-2018",
            }
        )
        self.assertTrue(success)
        self.assertIsNone(errors)
        
        pet = Pet.objects.get(pk=1)
        self.assertEqual(pet.weight, 25.0)

        pet.update_pet({"weight": 26.5})
        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.weight, 26.5)

    def test_update_pet_with_error(self):
        success, errors = Pet.save_pet(
            {
                "name": "Roma",
                "breed": "",
                "weight": 25.0,
                "birthday": "11-02-2018",
            }
        )
        self.assertTrue(success)
        self.assertIsNone(errors)
        
        pet = Pet.objects.get(pk=1)
        self.assertEqual(pet.weight, 25.0)

        with self.assertRaises(ValueError):
            pet.update_pet({"weight": -1})

        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.weight, 25.0)