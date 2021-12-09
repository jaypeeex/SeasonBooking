from django.db import models
from apps.apartments.models import Apartment
from apps.extra_services.models import ExtraService
from django.contrib.auth.models import User

class Booking(models.Model):
    booking_id = models.CharField(max_length=15, unique=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    is_canceled = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(default=None, null=True)
    total_amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    stay_from = models.DateField()
    stay_to = models.DateField()
    guests_number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    readonly_fields = ('stay_from',)

    class Meta:
        db_table = "booking"

class BookingExtraService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, default=None)
    extra_service = models.ForeignKey(ExtraService, on_delete=models.CASCADE, default=None)
    service_booking_total_amount = models.IntegerField()

    class Meta:
        db_table = "booking_extra_service"


class CheckIn(models.Model):
    booking_id = models.CharField(max_length=15)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    guests_number = models.IntegerField()
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    check_in_staff = models.CharField(max_length=50)

    class Meta:
        db_table = "check_in"