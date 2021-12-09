
from .forms import LoginForm
from .forms import CreateUserForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from .decorators import unauthenticated_user
from pprint import pprint

@unauthenticated_user
def user_register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request, 'Cuenta creada con éxito!')
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter().exists():
                if user.groups.filter()[0].name == 'customer':
                    return redirect('index')
                elif user.groups.filter()[0].name == 'admin':
                    return redirect('dashboard')
                elif user.groups.filter()[0].name == 'employee':
                    return redirect('dashboard')
            else:
                return redirect('logout')
        else:
            messages.error(request,'Usuario o contraseña incorrecta')
            pprint(vars(messages))

    form = LoginForm()
    context = {'form': form}

    return render(request, 'accounts/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')
