from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'color', 'size', 'description']
        labels = {
            "name": "Nombre",
            "color": "Color",
            "size": "Tamaño",
            "description": "Descripcion",
        }