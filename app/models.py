from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_client(data):
    """Valida que no se genere un cliente vacio en la veterinaria"""
    errors = {}

    name = data.get("name", "")
    phone = str(data.get("phone", ""))  
    email = data.get("email", "")
    city = data.get("city", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"
    elif not all(char.isalpha() or char.isspace() for char in name):
        errors["name"] = "El nombre solo puede contener letras y espacios"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    elif not phone.isdigit():
        errors["phone"] = "Por favor ingrese un telefono valido"
    elif not phone.startswith('54'):
        errors["phone"] = "El teléfono debe comenzar con 54"
            
    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email válido"
    elif not email.endswith("@vetsoft.com"):
        errors["email"] = "El email debe terminar en @vetsoft.com"
    elif email == "@vetsoft.com":
        errors["email"] = "El email no puede ser solo '@vetsoft.com'"

    if city == "" or city is None:
        errors["city"] = "Por favor ingrese una ciudad"
    elif city not in dict(City.choices):
        errors["city"] = "Ciudad no válida"

    return errors

class City(models.TextChoices):
    """
    Ciudades de los clientes.
    """ 
    ENSENADA = 'Ensenada', 'Ensenada'
    LA_PLATA = 'La Plata', 'La Plata'
    BERISSO = 'Berisso', 'Berisso'


def validate_medicine(data):
    """Valida que no se genere una medicina vacia en la veterinaria y  que la dosis este entre 1 y 10"""
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
            dosis = int(dosis)
            if dosis <= 0:
                errors['dosis'] = "La dosis debe ser mayor a cero"
            elif dosis  < 1:
                errors["dosis"] = "La dosis debe ser mayor o igual que 1"
            elif dosis > 10:
                errors["dosis"] = "La dosis debe ser menor que 10"
        except ValueError:
            errors["dosis"] = "La cantidad de dosis no es correcta,debe ser una cantidad entera"
    return errors

def validate_provider(data):
    """Valida que no se genere un proveedor vacio en la veterinaria"""
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
    """Valida que no se genere un producto vacio vacio en la veterinaria y que el precio de un producto sea mayor a 0"""
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
    """Valida que no se genere un veterinario vacio en la veterinaria"""
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    speciality= data.get("speciality","")
    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    
    if speciality == "" or speciality is None:
        errors["speciality"] = "Por favor seleccione una especialidad válida"
    elif speciality not in [choice[0] for choice in Vet.SPECIALITY_CHOICES.choices]:
        errors["speciality"] = "Especialidad no válida"

    return errors



class Client(models.Model):
    """
    Definicion de clase cliente y sus metodos
    """
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    city = models.CharField(max_length=50, choices=City, default=City.LA_PLATA)

    def __str__(self):
        """
        Devuelve una representación en cadena del objeto.

        Returns:
            Una cadena que representa el nombre del objeto.
        """
        return self.name

    @classmethod
    def save_client(cls, client_data):
        """
        Guarda un cliente en la base de datos.

        Args:
            client_data: un diccionario que contiene los datos del cliente.

        Returns:
            Una tupla (booleano, errores) donde el booleano indica el éxito de la operación
            y los errores contiene los errores de validación si los hay.
        """
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            city=client_data.get("city"),
        )

        return True, None

    def update_client(self, client_data):
        """
        Actualiza un cliente en la base de datos.

        Args:
            client_data: un diccionario que contiene los nuevos datos del cliente.

        Returns:
            Ninguno.
        """
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.city = client_data.get("city", "") or self.city

        self.save()
        return True, None
    
class Pet(models.Model):
    """
    Definicion de clase mascota y sus metodos
    """
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=50, blank=True)
    birthday = models.DateField()
    weight = models.DecimalField(max_digits=8, decimal_places=3)

    @classmethod
    def validate_pet(cls, data):
        """
        Valida los datos de la mascota. 
        """
        errors = {}

        name = data.get("name", "")
        name = data.get("name", "") 
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
        """
        Guarda una mascota en la base de datos.

        Args:
            pet_data: un diccionario que contiene los datos de la mascota.

        Returns:
            Una tupla (booleano, errores) donde el booleano indica el éxito de la operación
            y los errores contiene los errores de validación si los hay.
        """
        errors = cls.validate_pet(pet_data)
        if len(errors.keys()) > 0:
            return False, errors

        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=pet_data.get("birthday"),
            weight=pet_data.get("weight"),
        )

        return True, None

    def update_pet(self, pet_data):
        """
        Actualiza una mascota en la base de datos.

        Args:
            pet_data: un diccionario que contiene los nuevos datos de la mascota.

        Returns:
            Ninguno.
        """
        self.name = pet_data.get("name", "") or self.name
        self.breed = pet_data.get("breed", "") or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday

        self.save()
        return True, None

    def __str__(self):
        """
        Devuelve una representación en cadena del objeto.

        Returns:
            Una cadena que representa el nombre del objeto.
        """
        return self.name

class Medicine(models.Model):
    """
    Definicion de clase medicamento y sus metodos
    """
    name = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True)
    dosis = models.IntegerField()

    def __str__(self):
        """
        Devuelve una representación en cadena del objeto.

        Returns:
            Una cadena que representa el nombre del objeto.
        """
        return self.name
    
    @classmethod
    def save_medicine(cls, medicine_data):
        """
        Guarda un medicamento en la base de datos.

        Args:
            medicine_data: un diccionario que contiene los datos del medicamento.

        Returns:
            Una tupla (booleano, errores) donde el booleano indica el éxito de la operación
            y los errores contiene los errores de validación si los hay.
        """
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
        """
        Actualiza un medicamento en la base de datos.

        Args:
            medicine_data: un diccionario que contiene los nuevos datos del medicamento.

        Returns:
            Una tupla (booleano, errores) donde el booleano indica el éxito de la operación
            y los errores contiene los errores de validación si los hay.
        """
        errors = validate_medicine(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors
        
        self.name = medicine_data.get("name", "") or self.name
        self.descripcion = medicine_data.get("descripcion", "") or self.descripcion
        self.dosis = medicine_data.get("dosis", "") or self.dosis
        
        self.save()
    
        return True, None

class Provider(models.Model):
    """
    Definicion de clase proveedor y sus metodos
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address=models.CharField(max_length=100, blank=True)

    def __str__(self):
        """
        Devuelve una representación en cadena del objeto.

        Returns:
            Una cadena que representa el nombre del objeto.
        """
        return self.name

    @classmethod
    def save_provider(cls, provider_data):
        """
        Guarda un proveedor en la base de datos.

        Args:
            provider_data: un diccionario que contiene los datos del proveedor.

        Returns:
            Una tupla (booleano, errores) donde el booleano indica el éxito de la operación
            y los errores contiene los errores de validación si los hay.
        """
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
        """
        Actualiza un proveedor en la base de datos.

        Args:
            provider_data: un diccionario que contiene los nuevos datos del proveedor.

        Returns:
            Ninguno.
        """
        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email
        self.address = provider_data.get("address", "") or self.address
        self.save()
 
class Product(models.Model):
    """
    Definicion de clase producto y sus metodos
    """
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        """
        Devuelve una representación en cadena del objeto.

        Returns:
            Una cadena que representa el nombre del objeto.
        """
        return self.name
    
    @classmethod
    def save_product(cls, product_data):
        """
        Guarda un producto en la base de datos.

        Args:
            product_data: un diccionario que contiene los datos del producto.

        Returns:
            Una tupla (booleano, errores) donde el booleano indica el éxito de la operación
            y los errores contiene los errores de validación si los hay.
        """
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
        """
        Actualiza un producto en la base de datos.

        Args:
            product_data: un diccionario que contiene los nuevos datos del producto.

        Returns:
            Una tupla (booleano, errores) donde el booleano indica el éxito de la operación
            y los errores contiene los errores de validación si los hay.
        """
        errors = validate_product(product_data)  

        if len(errors.keys()) > 0:
            return False, errors
        
        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.type
        self.price = product_data.get("price", "") or self.price

        self.save()
        
        return True, None

class Vet(models.Model):
    """
    Definicion de clase veterinario y sus metodos
    """
    class SPECIALITY_CHOICES(models.TextChoices):
        CARDIOLOGIA="Cardiologia", _("Cardiologia")
        NEUROLOGIA="Neurologia", _("Neurologia")
        ONCOLOGIA="Oncologia", _("Oncologia")
        NUTRICION="Nutricion", _("Nutricion")
        CLINICA="Clinica", _("Clinica")

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    speciality = models.CharField(max_length=50, choices=SPECIALITY_CHOICES, default=SPECIALITY_CHOICES.CLINICA)

    def __str__(self):
        """
        Devuelve una representacion en cadena de objeto
        """
        return self.name

    @classmethod
    def save_vet(cls, data):
        """
        Guarda un veterinario
        """
        errors = validate_Vet(data)

        if len(errors.keys()) > 0:
            return False, errors
        
        Vet.objects.create (
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            speciality=data.get('speciality'),
        )
        return True, None 

    def update_vet(self, data):
        """
        Guarda la edicion de un veterinario
        """
        errors = validate_Vet(data)

        if len(errors.keys()) > 0:
            return False, errors
        self.name = data.get('name')
        self.email = data.get('email')
        self.phone = data.get('phone')
        self.speciality = data.get('speciality')
        self.save()
        return True, {}
       
