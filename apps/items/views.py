from django.shortcuts import render, redirect
from .forms import ItemForm
from django.contrib import messages

def create_item(request):
    item_form = ItemForm()

    if request.method == "POST":
        item_form = ItemForm(request.POST)
        if item_form.is_valid():
            instancia = item_form.save(commit=False)
            instancia.save()
            messages.success(request, 'artículo creado exitosamente')
            return redirect('create-item')

    return render(request, 'items/create_item.html', {'item_form': item_form})
