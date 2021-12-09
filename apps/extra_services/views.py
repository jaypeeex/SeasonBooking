from django.shortcuts import render, redirect
from .forms import ExtraServiceForm
from .models import ExtraService
from pprint import pprint

def register_extra_service(request):
    if request.method == 'POST':
        form = ExtraServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('extra_services_list')

    form = ExtraServiceForm()
    context = {'extra_service_form': form}

    return render(request, 'extra_services/extra_service.html', context)

def extra_services_list(request):
    extra_services = ExtraService.objects.all()
    context = {'extra_services': extra_services}
    return render(request, 'extra_services/extra_services_list.html', context)

def edit_extra_service(request, extra_service_id):

    extra_service_instance = ExtraService.objects.get(id=extra_service_id)
    extra_service_form = ExtraServiceForm(instance=extra_service_instance)

    if request.method == 'POST':
        extra_service_form = ExtraServiceForm(request.POST, instance=extra_service_instance)
        if extra_service_form.is_valid():
                extra_service_form.save()

                return redirect('extra_services_list')

    context = {
        'extra_service_form': extra_service_form
    }

    return render(request, 'extra_services/extra_service.html', context)

