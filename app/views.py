from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse
from .models import Client 
from .models import Pet
from .forms import PetForm
from .models import Medicine
from .forms import MedicineForm
from .models import Provider
from .forms import ProviderForm
from .models import Product
from .forms import ProductForm
from .models import Vet
from .forms import VetForm


def home(request):
    return render(request, "home.html")


def clients_repository(request):
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients})


def clients_form(request, id=None):
    if request.method == "POST":
        client_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if client_id == "":
            saved, errors = Client.save_client(request.POST)
        else:
            client = get_object_or_404(Client, pk=client_id)
            client.update_client(request.POST)

        if saved:
            return redirect(reverse("clients_repo"))

        return render(
            request, "clients/form.html", {"errors": errors, "client": request.POST}
        )

    client = None
    if id is not None:
        client = get_object_or_404(Client, pk=id)

    return render(request, "clients/form.html", {"client": client})


def clients_delete(request):
    client_id = request.POST.get("client_id")
    client = get_object_or_404(Client, pk=int(client_id))
    client.delete()

    return redirect(reverse("clients_repo"))

def pets_repository(request):
    pets = Pet.objects.all()
    return render(request, "pets/repository.html", {"pets": pets})

def pets_form(request, id=None):
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
        request, "pets/form.html", {"errors": errors, "form": form, "form_title": "Agregar Mascota", "form_action": "pets_form"}
    )

def pets_delete(request):
    pet_id = request.POST.get("pet_id")
    pet = get_object_or_404(Pet, pk=int(pet_id))
    pet.delete()
    return redirect(reverse("pets_repo"))


def medicines_repository(request):
    medicine = Medicine.objects.all()
    return render(request, "medicines/repository.html", {"medicines": medicine})

def medicines_form(request, id=None):
    errors = {}
    medicine = None

    if request.method == "POST":
        saved = True

        medicine_id = request.POST.get("id") if "id" in request.POST else None

        if medicine_id is None:
            saved, errors = Medicine.save_medicine(request.POST)
        else:
            medicine = get_object_or_404(Medicine, pk=medicine_id)
            medicine.update_medicine(request.POST)

        if saved:
            return redirect(reverse("medicines_repo"))
    else:
        if id is not None:
            medicine = get_object_or_404(Medicine, pk=id)

    form = MedicineForm(request.POST or None, instance=medicine)

    return render(
        request, "medicines/form.html", {"errors": errors, "form": form, "form_title": "Agregar Medicamento", "form_action": "medicines_form"}
    )


def medicines_delete(request):
    medicine_id = request.POST.get("medicine_id")
    medicine = get_object_or_404(Medicine, pk=int(medicine_id))
    medicine.delete()
    return redirect(reverse("medicines_repo"))

def provider_repository(request):
    providers = Provider.objects.all()
    return render(request, "provider/repository.html", {"providers": providers})

def provider_form(request, id=None):
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
            request, "provider/form.html", {"errors": errors, "provider": request.POST}
        )

    provider = None
    if id is not None:
        provider = get_object_or_404(Provider, pk=id)

    return render(request, "provider/form.html", {"provider": provider})
    errors = {}
    provider = None


def provider_delete(request):
    provider_id = request.POST.get("provider_id")
    provider = get_object_or_404(Provider, pk=int(provider_id))
    provider.delete()
    return redirect(reverse("provider_repo"))

def products_repository(request):
    products = Product.objects.all()
    return render(request, "products/repository.html", {"products": products})


def products_form(request, id=None):
    errors = {}
    product = None

    if request.method == "POST":
        saved = True

        product_id = request.POST.get("id") if "id" in request.POST else None

        if product_id is None:
            saved, errors = Product.save_product(request.POST)
        else:
            product = get_object_or_404(Product, pk=product_id)
            product.update_product(request.POST)

        if saved:
            return redirect(reverse("products_repo"))
    else:
        if id is not None:
            product = get_object_or_404(Product, pk=id)

    form = ProductForm(request.POST or None, instance=product)

    return render(
        request, "products/form.html", {"errors": errors, "form": form, "form_title": "Agregar Producto", "form_action": "products_form"}
    )
 
 
def products_delete(request):
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, pk=int(product_id))
    product.delete()

    return redirect(reverse("products_repo"))
def vet_repository(request):
    vet = Vet.objects.all()
    return render(request, "vet/repository.html", {"vet": vet})


def vet_form(request, id=None):
    if request.method == "POST":
        vet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if vet_id == "":
            saved, errors = Vet.save_vet(request.POST)
        else:
            vet = get_object_or_404(Vet, pk=vet_id)
            vet.update_vet(request.POST)

        if saved:
            return redirect(reverse("vet_repo"))

        return render(
            request, "vet/form.html", {"errors": errors, "vet": request.POST}
        )

    vet = None
    if id is not None:
        vet = get_object_or_404(Vet, pk=id)

    form = VetForm(request.POST or None, instance=vet)

    return render(request, "vet/form.html", {"vet": vet})


def vet_delete(request):
    vet_id = request.POST.get("vet_id")
    vet = get_object_or_404(Vet, pk=int(vet_id))
    vet.delete()

    return redirect(reverse("vet_repo"))
