from django import forms

from .models import Medicine, Pet, Product, Provider, Vet


class PetForm(forms.ModelForm):
    """
    Clase mascota del formulario
    """
    class Meta:
        """
        Define los metadatos del formulario
        """
        model = Pet
        fields = ['name', 'breed', 'weight', 'birthday']

class MedicineForm(forms.ModelForm):
    """
    Clase medicamento del formulario
    """
    class Meta:
        """
        Define los metadatos del formulario
        """
        model = Medicine
        fields = ['name', 'descripcion', 'dosis']

class ProviderForm(forms.ModelForm):
    """
    Clase proveedor del formulario
    """
    class Meta:
        """
        Define los metadatos del formulario
        """
        model = Provider
        fields = ['name', 'email', 'address']

class ProductForm(forms.ModelForm):
    """
    Clase producto del formulario
    """
    class Meta:
        """
        Define los metadatos del formulario
        """
        model = Product
        fields = ['name', 'type','price']
        
class VetForm(forms.ModelForm):
    """
    Clase veterinario del formulario
    """
    class Meta:
        """
        Define los metadatos del formulario
        """
        model = Vet
        fields = ['name', 'email', 'phone', 'speciality']
