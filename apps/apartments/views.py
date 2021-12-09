from .forms import ApartmentForm, ApartmentImageForm
from .models import Apartment, ApartmentImage, ApartmentExtraService
from django.shortcuts import render, redirect
from django.forms import formset_factory, modelformset_factory
from apps.extra_services.models import ExtraService
from apps.inventory.models import Inventory, InventoryItem
from apps.items.models import Item
from apps.accounts.decorators import allowed_users
from datetime import datetime
from pprint import pprint
from apps.inventory.forms import InventoryItemForm
from django.db import connection

def reporte_diario():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    fecha = datetime.now()
    ApartmentId = 1

    cursor.callproc("SP_SEL_REPORTEDIARIOGANANCIAS",[fecha, ApartmentId, out_cur])

    lista = []

    for fila in out_cur:
        lista.append(fila)

    return lista

def reporte_mensual():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    fecha = datetime.now()
    ApartmentId = 1

    cursor.callproc("SP_SEL_REPORTEMENSUALGANANCIAS",[fecha, ApartmentId, out_cur])

    lista = []

    for fila in out_cur:
        lista.append(fila)

    return lista

def reporte_anual():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    fecha = datetime.now()
    ApartmentId = 1

    cursor.callproc("SP_SEL_REPORTEANUALGANANCIAS",[fecha, ApartmentId, out_cur])

    lista = []

    for fila in out_cur:
        lista.append(fila)

    return lista

@allowed_users(allowed_roles=['admin'])
def register_apartment(request):
    pprint(reporte_diario())
    pprint(reporte_mensual())
    pprint(reporte_anual())

    apartment_form = ApartmentForm()
    ApartmentImageFormSet = formset_factory(ApartmentImageForm, extra=4)
    apartment_image_formset = ApartmentImageFormSet()

    if request.method == 'POST':
       apartment_form = ApartmentForm(request.POST)
       apartment_image_formset = ApartmentImageFormSet(request.POST, request.FILES)
       if apartment_form.is_valid():
           if apartment_image_formset.is_valid():
               apartment_form_instance = apartment_form.save(commit=False)
               inventory_instance = Inventory.objects.create(name='TEST', date=datetime.now())

               apartment_form_instance.inventory_id = inventory_instance.id
               apartment_form_instance.save()

               for f in apartment_image_formset:
                   formset_instance = f.save(commit=False)
                   formset_instance.apartment_id = apartment_form_instance.id
                   formset_instance.save()

               return redirect('apartment_list')

    context = {
       'apartment_form': apartment_form,
       'apartment_image_formset': apartment_image_formset
    }
    return render(request, "apartments/apartment.html", context)

@allowed_users(allowed_roles=['admin'])
def apartment_list(request):
    apartments = Apartment.objects.all()
    context = {'apartments': apartments}
    return render(request, 'apartments/apartment_list.html', context)


@allowed_users(allowed_roles=['admin'])
def edit_apartment(request, apartment_id):
    aparment_instance = Apartment.objects.get(id=apartment_id)
    apartment_form = ApartmentForm(instance=aparment_instance)

    ApartmentImageFormSet = modelformset_factory(ApartmentImage, fields=('imageFile',), extra=0)

    apartment_images_instances = ApartmentImage.objects.filter(apartment_id=apartment_id)

    apartment_image_formset = ApartmentImageFormSet(queryset=apartment_images_instances)

    if request.method == 'POST':
        apartment_form = ApartmentForm(request.POST, instance=aparment_instance)
        apartment_image_formset = ApartmentImageFormSet(request.POST, request.FILES)
        if apartment_form.is_valid():
            if apartment_image_formset.is_valid():
                apartment_form_instance = apartment_form.save()

                for f in apartment_image_formset:
                    formset_instance = f.save(commit=False)
                    formset_instance.apartment_id = apartment_form_instance.id
                    formset_instance.save()

        return redirect('apartment_list')

    context = {
        'apartment_form': apartment_form,
        'apartment_image_formset': apartment_image_formset
    }
    return render(request, "apartments/apartment.html", context)

@allowed_users(allowed_roles=['admin'])
def apartment_extra_services(request, apartment_id):
    extra_services = ExtraService.objects.all()
    apartment_extra_services = ApartmentExtraService.objects.filter(apartment_id=apartment_id)
    old_extra_services = []
    old_extra_services_ids = []
    for item in extra_services:
        extra_service = {}
        extra_service["id"] = item.id
        extra_service["is_enabled"] = False
        for service in apartment_extra_services:
            if service.extra_service_id == item.id:
                extra_service["is_enabled"] = True
        old_extra_services.append(extra_service)

    for item in apartment_extra_services:
        old_extra_services_ids.append(item.extra_service_id)

    if request.method == 'POST':
        new_extra_services = []
        for val, item in enumerate(extra_services):
            item_check = request.POST.get('checkbox-extra-service-'+str(val))

            extra_service = {}
            extra_service["id"] = item.id

            if item_check == 'on':
                extra_service["is_enabled"] = True
            else:
                extra_service["is_enabled"] = False

            new_extra_services.append(extra_service)

        for val, old_item in enumerate(old_extra_services):
            if new_extra_services[val] != old_item:
                if old_item["is_enabled"] == True and new_extra_services[val]["is_enabled"] == False:
                    ApartmentExtraService.objects.filter(extra_service_id=old_item["id"]).delete()
                else:
                    new_apartment_extra_service_obj = ApartmentExtraService(apartment_id=apartment_id, extra_service_id=old_item["id"])
                    new_apartment_extra_service_obj.save()

        return redirect('apartment_list')

    context = {
        'extra_services': extra_services,
        'apartment_extra_services': apartment_extra_services,
        'old_extra_services': old_extra_services,
        'old_extra_services_ids': old_extra_services_ids
    }

    return render(request, "apartments/apartment_extra_services.html", context)

@allowed_users(allowed_roles=['admin'])
def apartment_inventory(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)

    inventory_id = apartment.inventory.id
    items = Item.objects.all()
    inventory_items = InventoryItem.objects.filter(inventory_id=inventory_id)

    context = {
        'inventory_items': inventory_items,
        'items': items,
        'apartment': apartment
    }

    return render(request, "apartments/apartment_inventory.html", context)

@allowed_users(allowed_roles=['admin'])
def delete_inventory_item(request, apartment_id, inventory_item_id):

    apartment = Apartment.objects.get(id=apartment_id)
    InventoryItem.objects.filter(inventory_id=apartment.inventory.id).filter(id=inventory_item_id).delete()

    return redirect('apartment_inventory', apartment_id=apartment_id)

@allowed_users(allowed_roles=['admin'])
def create_inventory_item(request, inventory_id):
    inventory = Inventory.objects.get(id=inventory_id)
    inventoryItem_form = InventoryItemForm(initial={'inventory': inventory_id})
    apartment = Apartment.objects.get(inventory_id=inventory_id)

    if request.method == "POST":
        inventoryItem_form = InventoryItemForm(request.POST)
        if inventoryItem_form.is_valid():
            instancia = inventoryItem_form.save(commit=False)
            instancia.save()
            id = str(inventory_id)
            return redirect('apartment_inventory', apartment_id=apartment.id)

    context = {'inventory': inventory, 'form': inventoryItem_form}

    return render(request, 'apartments/create_inventory_item.html', context)
