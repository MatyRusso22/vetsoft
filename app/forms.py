from django import forms

from .models import Medicine, Pet, Product, Provider, Vet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'breed', 'weight', 'birthday']
        error_messages = {
            'name': {
                'required': 'Por favor ingrese un nombre',
            },
            'weight': {
                'required': 'Por favor ingrese un peso',
                'invalid': 'Por favor ingrese un peso válido',
            },
            'birthday': {
                'required': 'Por favor ingrese una fecha',
                'invalid': 'Por favor ingrese una fecha válida',
            },
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_weight(self):
        weight = self.cleaned_data.get("weight")
        if weight is not None and weight <= 0:
            raise forms.ValidationError("El peso debe ser mayor que 0")
        return weight
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
