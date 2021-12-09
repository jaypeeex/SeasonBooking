from django import forms
from .models import InventoryItem
from apps.items.models import Item

class InventoryItemForm(forms.ModelForm):
    item = forms.ModelChoiceField(queryset=Item.objects.all())

    class Meta:
        model = InventoryItem
        fields = ['quantity','item', 'inventory']
        labels = {
            "quantity": "Cantidad",
            "item" : "Item",
            "inventory":"Inventario",
            }

        widgets = {
            'inventory': forms.HiddenInput()
        }

