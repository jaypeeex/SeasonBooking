from django import forms
from .models import Booking, CheckIn


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BookingForm, self).__init__(*args, **kwargs)

    stay_from = forms.DateTimeField(input_formats=['%d-%m-%Y'], label='Desde', required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    stay_to = forms.DateTimeField(input_formats=['%d-%m-%Y'], label='Hasta', required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    selected_extra_services = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Booking
        fields = ['stay_from', 'stay_to', 'guests_number', 'apartment']
        labels = {
            "stay_from": "Desde",
            "stay_to": "Hasta",
            "guests_number": "Cantidad de huéspedes"
        }

        widgets = {
            'guests_number': forms.TextInput(attrs={'readonly': 'readonly'}),
            'apartment': forms.HiddenInput()
        }


class CheckInForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CheckInForm, self).__init__(*args, **kwargs)

    arrival_date = forms.DateTimeField(
        input_formats=['%d-%m-%Y'],
        label='Desde', required=True,
        widget=forms.TextInput(attrs={'class': 'datepicker'})
    )
    departure_date = forms.DateTimeField(
        input_formats=['%d-%m-%Y'],
        label='Hasta', required=True,
        widget=forms.TextInput(attrs={'class': 'datepicker'})
    )

    arrival_time = forms.TimeField(
        input_formats=['%H:%M'],
        label='Hora de llegada', required=True,
        widget=forms.TextInput(attrs={'class': 'timepicker'})
    )
    departure_time = forms.TimeField(
        input_formats=['%H:%M'],
        label='Hora de salida', required=True,
        widget=forms.TextInput(attrs={'class': 'timepicker'})
    )

    class Meta:
        model = CheckIn
        fields = '__all__'
        widgets = {
            'arrival_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'departure_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'arrival_time': forms.TextInput(attrs={'class': 'timepicker'}),
            'departure_time': forms.TextInput(attrs={'class': 'timepicker'}),
            'check_in_staff': forms.TextInput(attrs={'readonly': 'readonly'})
        }
        labels = {
            "booking_id": "ID de la reserva",
            "arrival_date": "Fecha de llegada",
            "departure_date": "Fecha de salida",
            "arrival_time": "Hora de llegada",
            "departure_time": "Hora de salida",
            "guests_number": "Cantidad de huéspedes",
            "email": "Email",
            "phone": "Teléfono",
            "check_in_staff": "Recibido(s) por: "
        }


