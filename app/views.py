from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import PetForm
from .models import City, Client, Medicine, Pet, Product, Provider, Vet


def home(request):
    """
    Renderiza la página de inicio.
    """
    return render(request, "home.html")

def clients_repository(request):
    """
    Muestra el repositorio de clientes.
    """
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients})

def clients_form(request, id=None):
    """
    Maneja el formulario para crear o actualizar un cliente.
    """
    cities = City.choices
    if request.method == "POST":
        client_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if client_id == "":
            saved, errors = Client.save_client(request.POST)
        else:
            client = get_object_or_404(Client, pk=client_id)
            saved,errors=client.update_client(request.POST)
        if saved:
            return redirect(reverse("clients_repo"))
        return render(
            request, "clients/form.html", {"errors": errors, "client": request.POST, "cities": cities }
        )

    client = None
    if id is not None:
        client = get_object_or_404(Client, pk=id)

    return render(request, "clients/form.html", {"client": client, "cities": cities})

def clients_delete(request):
    """
    Elimina un cliente.
    """
    client_id = request.POST.get("client_id")
    client = get_object_or_404(Client, pk=int(client_id))
    client.delete()

    return redirect(reverse("clients_repo"))

def pets_repository(request):
    """
    Muestra el repositorio de mascotas.
    """
    pets = Pet.objects.all()
    return render(request, "pets/repository.html", {"pets": pets})

def pets_form(request, id=None):
    """
    Maneja el formulario para crear o actualizar una mascota.
    """
    errors = {}
    pet = None
    saved = True

    if request.method == "POST":
        pet_id = request.POST.get("id") if "id" in request.POST else None

        if pet_id is None:
            saved, errors = Pet.save_pet(request.POST)
        else:
            pet = get_object_or_404(Pet, pk=pet_id)
            try:
                pet.update_pet(request.POST)
            except ValueError as e:
                errors["weight"] = str(e)
                saved = False
        if saved:
            return redirect(reverse("pets_repo"))
    else:
        if id is not None:
            pet = get_object_or_404(Pet, pk=id)
    form = PetForm(request.POST or None, instance=pet)
    return render(
        request, "pets/form.html", {"errors": errors, "form": form, "form_title": "Agregar Mascota", "form_action": "pets_form"},
    )

def pets_delete(request):
    """
    Elimina una mascota.
    """
    pet_id = request.POST.get("pet_id")
    pet = get_object_or_404(Pet, pk=int(pet_id))
    pet.delete()
    return redirect(reverse("pets_repo"))

def medicines_repository(request):
    """
    Muestra el repositorio de medicamentos.
    """
    medicine = Medicine.objects.all()
    return render(request, "medicines/repository.html", {"medicines": medicine})

def medicines_form(request, id=None):
    """
    Maneja el formulario para crear o actualizar un medicamento.
    """
    if request.method == "POST":
        saved = True
        errors = {}
        medicine = None
        medicine_id = request.POST.get("id", "") 
        
        if medicine_id == "":
            saved, errors = Medicine.save_medicine(request.POST)
        else:
            medicine = get_object_or_404(Medicine, pk=medicine_id)
            medicine.update_medicine(request.POST)
        if saved:
            return redirect(reverse("medicines_repo"))
        return render (request, "medicines/form.html", {"errors": errors, "medicines": request.POST})
    
    medicine=None
    if id is not None: 
        medicine=get_object_or_404(Medicine, pk=id) 
    return render (request, "medicines/form.html", { "medicines": medicine})

def medicines_delete(request):
    """
    Elimina un medicamento.
    """
    medicine_id = request.POST.get("medicine_id")
    medicine = get_object_or_404(Medicine, pk=int(medicine_id))
    medicine.delete()
    return redirect(reverse("medicines_repo"))

def provider_repository(request):
    """
    Muestra el repositorio de proveedores.
    """
    providers = Provider.objects.all()
    return render(request, "provider/repository.html", {"providers": providers})

def provider_form(request, id=None):
    """
    Maneja el formulario para crear o actualizar un proveedor.
    """
    if request.method == "POST":
        provider_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if provider_id == "":
            saved, errors = Provider.save_provider(request.POST)
        else:
            provider = get_object_or_404(Provider, pk=provider_id)
            provider.update_provider(request.POST)

        if saved:
            return redirect(reverse("provider_repo"))

        return render(
            request, "provider/form.html", {"errors": errors, "provider": request.POST},
        )
    provider = None
    if id is not None:
        provider = get_object_or_404(Provider, pk=id)

    return render(request, "provider/form.html", {"provider": provider})

def provider_delete(request):
    """
    Elimina un proveedor.
    """
    provider_id = request.POST.get("provider_id")
    provider = get_object_or_404(Provider, pk=int(provider_id))
    provider.delete()
    return redirect(reverse("provider_repo"))

def products_repository(request):
    """
    Muestra el repositorio de productos.
    """
    products = Product.objects.all()
    return render(request, "products/repository.html", {"products": products})

def products_form(request, id=None):
    """
    Maneja el formulario para crear o actualizar un producto.
    """
    if request.method == "POST":
        product_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if product_id == "":
            saved, errors = Product.save_product(request.POST)
        else:
            product = get_object_or_404(Product, pk=product_id)
            saved, errors = product.update_product(request.POST)
        if saved:
            return redirect(reverse("products_repo"))
        return render(
            request, "products/form.html", {"errors": errors, "product": request.POST},
        )
    
    product = None
    if id is not None:
        product = get_object_or_404(Product, pk=id)
    return render(request, "products/form.html", {"product": product})

def products_delete(request):
    """
    Elimina un producto.
    """
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, pk=int(product_id))
    product.delete()
    return redirect(reverse("products_repo"))

def vet_repository(request):
    """
    Muestra el repositorio de veterinarios.
    """
    vets = Vet.objects.all()
    return render(request, "vet/repository.html", {"vets": vets})

def vet_form(request, id=None):
    """
    Maneja el formulario para crear o actualizar un veterinario.
    """
    specialities = Vet.SPECIALITY_CHOICES.choices
    if request.method == "POST":
        vet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if vet_id == "":
            saved, errors = Vet.save_vet(request.POST)
        else:
            vet = get_object_or_404(Vet, pk=vet_id)
            saved, errors= vet.update_vet(request.POST)

        if saved:
            return redirect(reverse("vet_repo"))

        return render(
            request, "vet/form.html", {"errors": errors, "vet": request.POST, "specialities" : specialities},
        )

    vet = None
    if id is not None:
        vet = get_object_or_404(Vet, pk=id)
    return render(request, "vet/form.html", {"vet": vet, "specialities" : specialities})

def vet_delete(request):
    """
    Elimina un veterinario.
    """
    vet_id = request.POST.get("vet_id")
    vet = get_object_or_404(Vet, pk=int(vet_id))
    vet.delete()
    return redirect(reverse("vet_repo"))