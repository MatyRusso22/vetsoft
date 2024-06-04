from django import forms

from .models import Medicine, Pet, Product, Provider, Vet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'breed', 'weight', 'birthday']

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'descripcion', 'dosis']

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'email', 'address']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'type','price']
        
class VetForm(forms.ModelForm):
    class Meta:
        model = Vet
        fields = ['name', 'email', 'phone', 'speciality']
