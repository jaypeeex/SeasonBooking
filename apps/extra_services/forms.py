from django import forms
from .models import ExtraService, ExtraServiceCategory

class ExtraServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ExtraServiceForm, self).__init__(*args, **kwargs)

    extra_service_category = forms.ModelChoiceField(label="Categoría" , queryset=ExtraServiceCategory.objects.all(),  empty_label="Selecciona una opción")

    class Meta:
        model = ExtraService
        fields = ['name', 'description', 'price', 'extra_service_category']
        labels = {
            "name": "Nombre",
            "description": "Descripción",
            "price": "Precio",
            "extra_service_category": "Categoría"
        }
        widgets = {
            'description': forms.Textarea(attrs={'class': 'materialize-textarea'}),
            'price': forms.NumberInput(attrs={'onkeydown': 'return event.keyCode !== 69'})
        }

