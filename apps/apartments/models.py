from django.db import models
from apps.extra_services.models import ExtraService
from apps.inventory.models import Inventory

class Apartment(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    rate = models.IntegerField()
    capacity = models.IntegerField()
    address = models.CharField(max_length=100, default=None)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, default=None)

    class Meta:
        db_table = "apartment"

class ApartmentImage(models.Model):
    imageFile = models.ImageField(upload_to='apartments', blank=False)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, default=None)

    class Meta:
        db_table = "apartment_image"

class ApartmentExtraService(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, default=None)
    extra_service = models.ForeignKey(ExtraService, on_delete=models.CASCADE, default=None)
    class Meta:
        db_table = "apartment_extra_service"





