from django import forms
from .models import Apartment
from .models import ApartmentImage



class ApartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ApartmentForm, self).__init__(*args, **kwargs)

    capacity = forms.ChoiceField(label="Capacidad" ,choices=(
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10')))

    class Meta:
        model = Apartment
        fields = ['name', 'description', 'rate', 'capacity', 'address']
        labels = {
            "name": "Nombre",
            "description": "Descripción",
            "rate": "Tarifa",
            "capacity": "Capacidad",
            "address": "Dirección",
        }

        widgets = {
            'description': forms.Textarea(attrs={'class': 'materialize-textarea'}),
            'rate': forms.NumberInput(attrs={'min':1,'max': 999999999,'type': 'number'})
        }


class ApartmentImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ApartmentImageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ApartmentImage
        fields = ['imageFile']
        labels = {
            "imageFile": "Imagen"
        }
        widgets = {
            'imageFile': forms.FileInput(attrs={'class': 'dropify', 'required': 'required'}),
        }



