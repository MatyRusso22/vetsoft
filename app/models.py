from django.db import models


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
    else: 
        try:
            dosis = float(dosis)
            if dosis <= 0:
                errors['dosis'] = "La dosis debe ser mayor a cero"
            elif dosis  < 1:
                errors["dosis"] = "La dosis debe ser mayor o igual que 1"
            elif dosis > 10:
                errors["dosis"] = "La dosis debe ser menor que 10"
        except ValueError:
            errors["dosis"] = "La cantidad de dosis no es correcta"
    return errors

def validate_provider(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    address=data.get("address","")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"
    
    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    if address == "":
        errors["address"] = "Por favor ingrese una dirección"
    return errors


def validate_product(data):
    errors = {}
    
    name = data.get("name","")
    type = data.get("type","")
    price = data.get("price","")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre para el producto"
        
    if type =="":
        errors["type"] = "Por favor ingrese el tipo del producto"

    if price == "" :
        errors["price"] = "Por favor ingrese el precio del producto"
    else:
        try: 
            if float(price) <= 0:
                errors["price"] = "Por favor ingrese un precio del producto mayor que cero"
        except ValueError:
            errors["price"] = "Por favor ingrese un precio valido para el producto"
  
    return errors


def validate_Vet(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    speciality = data.get("speciality", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if speciality == "":
        errors["speciality"] = "Por favor ingrese una especialidad"
 

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
    breed = models.CharField(max_length=50, blank=True)
    birthday = models.DateField()
    weight = models.DecimalField(max_digits=8, decimal_places=3)

    @classmethod
    def validate_pet(cls, data):
        errors = {}

        name = data.get("name", "")
        breed = data.get("breed", "")
        birthday = data.get("birthday", "")
        weight = data.get("weight", "")
        if birthday == "":
                errors["birthday"] = "Por favor ingrese una fecha"

        if name == "":
            errors["name"] = "Por favor ingrese un nombre"

        if weight == "":
            errors["weight"] = "Por favor ingrese un peso"
        else:
            if (float(weight) <= 0):
                errors["weight"] = "El peso debe ser mayor que 0"
        return errors

    @classmethod
    def save_pet(cls, pet_data):
        errors = cls.validate_pet(pet_data)
        if len(errors.keys()) > 0:
            return False, errors

        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=pet_data.get("birthday"),
            weight=pet_data.get("weight")
        )

        return True, None

    def update_pet(self, pet_data):
        self.name = pet_data.get("name", "") or self.name
        self.breed = pet_data.get("breed", "") or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday

        self.save()
        return True, None

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True)
    dosis = models.FloatField()

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
        errors = validate_medicine(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors
        
        self.name = medicine_data.get("name", "") or self.name
        self.descripcion = medicine_data.get("descripcion", "") or self.descripcion
        self.dosis = medicine_data.get("dosis", "") or self.dosis
        self.save()
    
        return True, None

class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address=models.CharField(max_length=100, blank=True)

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
            address=provider_data.get("address"),
        )

        return True, None

    def update_provider(self, provider_data):
        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email
        self.address = provider_data.get("address", "") or self.address
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
        errors = validate_product(product_data)  

        if len(errors.keys()) > 0:
            return False, errors
        
        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.type
        self.price = product_data.get("price", "") or self.price

        self.save()
        
        return True, None

class Vet(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    speciality = models.CharField(max_length=100, default='General')

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
            speciality=vet_data.get("speciality"),          
        )

        return True, None

    def update_vet(self, vet_data):
        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email  
        self.phone = vet_data.get("phone", "") or self.phone
        self.speciality = vet_data.get("speciality", "") or self.speciality  
        self.save()
 
class EspecialidadVeterinario(models.TextChoices):
    GENERAL = 'General', 'General'
    CIRUGIA = 'Cirugía', 'Cirugía'
    DERMATOLOGIA = 'Dermatología', 'Dermatología'
    ODONTOLOGIA = 'Odontología', 'Odontología'
    OTRA = 'Otra', 'Otra'
       
