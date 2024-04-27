from django import forms
from .models import Pet
from .models import Medicine
from .models import Provider
from .models import Vet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'breed', 'birthday']

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'descripcion', 'dosis']

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'email']

class VetForm(forms.ModelForm):
    class Meta:
        model = Vet
        fields = ['name', 'email', 'phone']