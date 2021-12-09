from django.shortcuts import render, redirect
from apps.apartments.models import Apartment, ApartmentImage, ApartmentExtraService
from apps.bookings.models import Booking, BookingExtraService
from apps.extra_services.models import ExtraService
from django.http import JsonResponse, HttpResponse
from .forms import BookingForm, CheckInForm
from datetime import datetime, timedelta
from random import randrange
import requests, uuid
from django.views.decorators.csrf import csrf_exempt
from apps.accounts.decorators import admin_only
from django.urls import reverse
from pprint import pprint
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from apps.accounts.decorators import allowed_users
from django.contrib import messages
from django.db import connection

def index(request):

    apartments = Apartment.objects.all()
    data = []

    for apartment in apartments.iterator():
        apartment_image_object = ApartmentImage.objects.filter(apartment_id=apartment.id).first()
        apartment_data_image = {}
        apartment_data_image['apartment'] = apartment
        apartment_data_image['apartment_image'] = apartment_image_object
        data.append(apartment_data_image)

    context = {
        'data': data
    }
    return render(request, 'index.html', context)

@csrf_exempt
@allowed_users(allowed_roles=['admin', 'employee'])
def dashboard(request):

    apartments = Apartment.objects.all()
    data = []

    for apartment in apartments.iterator():
        apartment_image_object = ApartmentImage.objects.filter(apartment_id=apartment.id).first()
        apartment_data_image = {}
        apartment_data_image['apartment'] = apartment
        apartment_data_image['apartment_image'] = apartment_image_object
        data.append(apartment_data_image)

    context = {
        'data': data
    }

    if request.user.groups.filter()[0].name == 'employee':
        return render(request, 'employee/dashboard.html', context)
    elif request.user.groups.filter()[0].name == 'admin':
        return render(request, 'admin/dashboard.html', context)




def book_apartment(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    apartment_images = ApartmentImage.objects.filter(apartment_id=apartment.id)

    active_bookings = Booking.objects.filter(stay_from__gt=datetime.now()).filter(is_paid=True).values('stay_from', 'stay_to').order_by('stay_from')
    unavailable_dates = []
    for dates_range in active_bookings:
        delta = dates_range["stay_to"] - dates_range["stay_from"]
        for i in range(delta.days + 1):
            day = dates_range["stay_from"] + timedelta(days=i)
            if day not in unavailable_dates:
                unavailable_dates.append(day)

    context = {
        'apartment': apartment,
        'apartment_images': apartment_images,
        'loop_times': range(1, apartment.capacity+1),
        'unavailable_dates': unavailable_dates
    }

    return render(request, 'bookings/book_apartment.html', context)

def check_availability(request):
    check_in_date = request.POST.get("check_in_date")
    check_out_date = request.POST.get("check_out_date")
    number_guests = request.POST.get("number_guests")
    print(check_in_date)
    if 1==1:
        if request.is_ajax():
            availability_response = {'check_in_date': check_in_date, 'check_out_date': check_out_date, 'number_guests': number_guests };
            return JsonResponse(availability_response, status=200)
        else:
            message = "Not ajax"
            return HttpResponse(status=500)
    else:
        message = "There was an error"
        return HttpResponse(status=500)

@allowed_users(allowed_roles=['customer'])
def booking_confirm(request, apartment_id):
    if request.method == 'POST':
        apartment = Apartment.objects.get(id=apartment_id)
        apartment_image= ApartmentImage.objects.filter(apartment_id=apartment.id).first()
        check_in_date = request.POST.get('check-in-date')
        check_out_date = request.POST.get('check-out-date')
        guests_number = request.POST.get('number-guests')
        booking = Booking(
            stay_from=check_in_date,
            stay_to=check_out_date,
            guests_number=guests_number,
            apartment_id=apartment_id)
        booking_form = BookingForm(instance=booking)
        apartment_extra_services = ApartmentExtraService.objects.filter(apartment_id=apartment_id)


        check_in_date = datetime.strptime(check_in_date, "%d-%m-%Y").date()
        check_out_date =datetime.strptime(check_out_date, "%d-%m-%Y").date()

        stay_days = (check_out_date-check_in_date).days

        context = {
            'booking_form': booking_form,
            'apartment': apartment,
            'apartment_image': apartment_image,
            'apartment_extra_services': apartment_extra_services,
            'subtotal_amount': stay_days*apartment.rate
        }

        return render(request, 'bookings/confirm_booking.html', context)

@allowed_users(allowed_roles=['customer'])
def redirect_to_payment(request):

    if request.method=='POST':

        booking_form = BookingForm(request.POST)

        if booking_form.is_valid():
            check_in_date = booking_form.cleaned_data['stay_from'].date()
            check_out_date = booking_form.cleaned_data['stay_to'].date()
            stay_days = (check_out_date - check_in_date).days
            selected_extra_services = booking_form.cleaned_data["selected_extra_services"]
            selected_extra_services = selected_extra_services.split(',')
            user = request.user

            booking_object = booking_form.save(commit=False)

            generated_id = (uuid.uuid4().hex[:8]).upper()

            while Booking.objects.filter(booking_id=generated_id).count() > 0:
                generated_id = (uuid.uuid4().hex[:8]).upper()

            booking_object.booking_id = generated_id
            booking_object.total_amount = stay_days*booking_object.apartment.rate
            booking_object.created_at = datetime.now()
            booking_object.modified_at = datetime.now()
            booking_object.user = user
            booking_object.is_paid = False
            booking_object.save()

            if selected_extra_services[0] != '0':
                for extra_service_id in selected_extra_services:
                    extra_service = ExtraService.objects.get(id=extra_service_id)
                    booking_extra_service = BookingExtraService(
                        booking_id=booking_object.id,
                        extra_service_id=extra_service_id,
                        service_booking_total_amount=extra_service.price
                    )
                    booking_extra_service.save()
                    booking_object.total_amount = booking_object.total_amount+extra_service.price
                    booking_object.save()



            url = 'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.0/transactions'
            headers = {
                'Tbk-Api-Key-Id': '597055555532',
                'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
            }
            data = {
                'buy_order': str(booking_object.booking_id),
                "session_id": str(booking_object.booking_id),
                "amount": float(booking_object.total_amount),
                "return_url": str(request.build_absolute_uri(reverse('webpay_return')))
            }

            r = requests.post(url, headers=headers, json=data)

            json_response = r.json()
            token_ws = json_response['token']
            url = json_response['url']

            context = {
                'token_ws': token_ws,
                'url': url
            }
            return render(request, 'bookings/payment/webpay_redirect.html', context)


@csrf_exempt
def webpay_return(request):
    token = str(request.POST.get('token_ws'))

    if token == 'None':
        failed_buy_order = request.POST.get('TBK_ORDEN_COMPRA')
        deleted_booking = Booking.objects.get(booking_id=failed_buy_order)
        BookingExtraService.objects.filter(booking_id=deleted_booking.id).delete
        deleted_booking.delete()
        return redirect('payment_failed')

    else:
        url = 'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.0/transactions/'+token
        headers = {
            'Tbk-Api-Key-Id': '597055555532',
            'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
        }

        r = requests.put(url, headers=headers)
        print(r.json())
        if r.status_code == 200:
            json_response = r.json()
            if json_response['response_code'] == 0:
                paid_booking_id = json_response['buy_order']
                booking = Booking.objects.get(booking_id=paid_booking_id)
                booking.is_paid = True
                booking.save()
                template = loader.render_to_string(
                    'mails/booking_confirmation.html',
                    {
                        'booking': booking
                    }
                )
                html_message = template
                email_subject = 'Confirmación de Reserva'
                to_list = str(booking.user.email)
                mail = EmailMultiAlternatives(
                    email_subject, 'Hola '+str(booking.user.username), 'debrisonne_notification', [to_list])
                mail.attach_alternative(html_message, "text/html")

                mail.send(fail_silently=False)
                return redirect('payment_success')
            else:

                return redirect('payment_failed')
        else:
            return redirect('payment_failed')


def payment_success(request):
    return render(request, 'bookings/payment/success.html')


def payment_failed(request):
    return render(request, 'bookings/payment/fail.html')

def check_in(request):
    check_in_form = CheckInForm(initial={'check_in_staff': request.user.username})
    if request.method == 'POST':
        check_in_form = CheckInForm(request.POST)
        if check_in_form.is_valid():
            booking_id = request.POST.get('booking_id')
            booking = Booking.objects.filter(booking_id=booking_id)
            if not booking:
                messages.error(request, 'No existe ninguna reserva con el código ingresado')
                return redirect('check_in')
            else:
                if booking.first().is_canceled == True:
                    messages.error(request, 'No fue imposible ingresar el check-in ya que la reserva está anulada')
                    return redirect('check_in')
                else:
                    check_in_form.save()
                    messages.success(request, 'Formulario de check-in ingresado correctamente!')
                    return redirect('check_in')


    context = {
        'check_in_form': check_in_form
    }
    return render(request, 'employee/check_in.html', context)


def reservas_historicas(user_id):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    UserId = user_id

    cursor.callproc("SP_SEL_HISTORICORESERVAS", [UserId, out_cur])

    lista = []

    for fila in out_cur:
        lista.append(fila)

    return lista


def historical_booking(request):
    h_bookings = reservas_historicas(request.user.id)
    context = {
        'user': request.user,
        'h_bookings': h_bookings,
    }
    return render(request, 'bookings/historical_booking.html', context)




