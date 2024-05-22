from django.db import models
from datetime import datetime


def validate_client(data):
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors

def validate_pet(data):
    errors = {}

    name = data.get("name", "")
    breed = data.get("breed", "")
    weight = data.get("weight", "")
    birthday = data.get("birthday", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre para la mascota"

    if birthday == "":
        errors["birthday"] = "Por favor ingrese la fecha de nacimiento de la mascota"
    else:
        try:
            datetime.strptime(birthday, "%d-%m-%Y")
        except ValueError:
            errors["birthday"] = "La fecha de nacimiento debe tener el formato DD-MM-YYYY"

    if weight == "":
        errors["weight"] = "Por favor ingrese el peso de la mascota"
    else:
        try:
            weight = float(weight)
            if weight < 0:
                errors["weight"] = "El peso no puede ser menor a 0"
        except ValueError:
            errors["weight"] = "El peso debe ser un número válido"

    return errors

def validate_medicine(data):
    errors = {}

    name = data.get("name", "")
    descripcion = data.get("descripcion", "")
    dosis = data.get("dosis", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre para el medicamento"

    if descripcion == "":
        errors["descripcion"] = "Por favor ingrese una descripcion"
    
    if dosis == "":
        errors["dosis"] = "Por favor ingrese una dosis"

    return errors

def validate_provider(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"
    
    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


def validate_product(data):
    errors = {}
    name = data.get("name","")
    type = data.get("type","")
    price = data.get("price","")

    if name == "":
        errors['name'] = 'Por favor ingrese un nombre para el producto'
    if type == "":
        errors['type'] = 'Por favor ingrese el tipo del producto'
    if price == "":
        errors['price'] = 'Por favor ingrese el precio del producto'
    else:
        try:
            price_float = float(price)
            if price_float <= 0:
                errors['price'] = 'Por favor ingrese un precio del producto mayor que cero'
        except ValueError:
            errors['price'] = 'Por favor ingrese un precio válido para el producto'

    return errors


def validate_Vet(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
 

    return errors


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=client_data.get("address"),
        )

        return True, None

    def update_client(self, client_data):
        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "") or self.address

        self.save()

class Pet(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, blank=True)
    birthday = models.DateField()
    weight = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    @classmethod
    def save_pet(cls, pet_data):
        errors = validate_pet(pet_data)
        if errors:
            return False, errors
        
        birthday = datetime.strptime(pet_data["birthday"], "%d-%m-%Y").date()

        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=birthday,
            weight=float(pet_data.get("weight")),
        )
        return True, None

    def update_pet(self, pet_data):
        if "birthday" in pet_data and pet_data["birthday"]:
            self.birthday = datetime.strptime(pet_data["birthday"], "%d-%m-%Y").date()
        if "weight" in pet_data:
            weight = float(pet_data["weight"])
            if weight < 0:
                raise ValueError("El peso no puede ser menor que 0")
            self.weight = weight
        self.name = pet_data.get("name", self.name)
        self.breed = pet_data.get("breed", self.breed)
        self.save()

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True)
    dosis = models.IntegerField()

    def __str__(self):
        return self.name
    
    @classmethod
    def save_medicine(cls, medicine_data):
        errors = validate_medicine(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors

        Medicine.objects.create(
            name=medicine_data.get("name"),
            descripcion=medicine_data.get("descripcion"),
            dosis=medicine_data.get("dosis"),
        )

        return True, None

    def update_medicine(self, medicine_data):
        self.name = medicine_data.get("name", "") or self.name
        self.descripcion = medicine_data.get("descripcion", "") or self.descripcion
        self.dosis = medicine_data.get("dosis", "") or self.dosis

        self.save()

class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

    @classmethod
    def save_provider(cls, provider_data):
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        Provider.objects.create(
            name=provider_data.get("name"),
            email=provider_data.get("email"),
        )

        return True, None

    def update_provider(self, provider_data):
        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email
        
        self.save()
 
class Product(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.name
    
    @classmethod
    def save_product(cls, product_data):
        errors = validate_product(product_data)
        
        if len(errors.keys()) > 0:
            return False, errors

        Product.objects.create(
            name=product_data.get("name"),
            type=product_data.get("type"),
            price=product_data.get("price"),
        )  
        return True, None

    def update_product(self, product_data):
        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.descripcion
        self.price = product_data.get("price", "") or self.price

        self.save()

class Vet(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    @classmethod
    def save_vet(cls, vet_data):
        errors = validate_Vet(vet_data)
        if len(errors.keys()) > 0:
            return False, errors
            
        Vet.objects.create(
            name=vet_data.get("name"),
            email=vet_data.get("email"),
            phone=vet_data.get("phone"),
                      
        )

        return True, None

    def update_vet(self, vet_data):
        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email  
        self.phone = vet_data.get("phone", "") or self.phone
          
        self.save()
 

       
