# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile
# Modificar al inicio
from .forms import (RegistroUserForm,EditarEmailForm,EditarContrasenaForm)

# Create your views here.
def registro_usuario_view(request):
    if request.method == 'POST':
        #Si el method es post, obtenemos los datos del formulario
        form = RegistroUserForm(request.POST, request.FILES)

        #Comprobamos si el formulario es valido
        if form.is_valid():
            #En caso de ser valido obtenemos los datos del formulario
            #form-cleaned_data obtiene los datos limpios y los pone en un diccionario con pares clave/valor, donde
            #clave es el nombre del campo del formulario y el valor es el valor si existe
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')
            photo = cleaned_data.get('photo')
            #E instanciamos un objeto User, con el username y el password
            user_model = User.objects.create_user(username=username, password=password)
            #añadimos el email
            user_model.email = email
            #Y guardamos el objeto, esto guardara los datos en la db
            user_model.save()
            #Ahora, creamos un objeto UserProfile, aunque no haya incluido una imagen, ya quedara la referencia en la db
            user_profile = UserProfile()
            #Al campo user le asignamos el objeto user_model
            user_profile.user = user_model
            #y le asignamos la photo(el campo permite los datos null
            user_profile.photo = photo
            #POr último guardamos tambien el objeto USerProfile
            user_profile.save()
            #Ahora redireccionamos a la página accounts/gracias.html. pero lo hacemos con redirect
            #return redirect(reverse('accounts.gracias', kwargs={'username': username}))
            return render(request, 'accounts/gracias.html')
    else:
        #SI el método es Get, instanciamos un objeto REgistroUSerForm vacio
        form = RegistroUserForm()
    #CReamos el contexto
    context = {'form': form}
    #Y mostramos los datos
    return render(request, 'accounts/registro.html', context)

def gracias_view(): #request, username
    return render(request, 'account/gracias.html')#, {'username': username}

@login_required
def index_view(request):
    return render(request, 'accounts/index.html')

def login_view(request):
    #si el usuario esta loggeado lo redireccionamos a index_view
    if request.user.is_authenticated():
        return redirect(reverse('accounts.index'))

    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('accounts.index'))
            else:
                #REdireccionar informando que la cuenta esta inactiva
                mensaje = 'El usuario esta desactivado'
                pass
        mensaje = 'Nombre de usuario o contraseña no valido'
    return render(request, 'accounts/login.html', {'mensaje': mensaje})

def logout_view(request):
    logout(request)
    messages.success(request, 'Te has desconectado con éxito')
    return render(request, 'accounts/login.html')

@login_required
def editar_email(request):
    if request.method == 'POST':
        form = EditarEmailForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'El email ha sido cambiado con exito!.')
            return redirect(reverse('accounts.index'))
    else:
        form = EditarEmailForm(
            request=request,
            initial={'email': request.user.email})
    return render(request, 'accounts/editar_email.html', {'form': form})


# Añadir al inicio
from django.contrib.auth.hashers import make_password


# Añadir al final
@login_required
def editar_contrasena(request):
    if request.method == 'POST':
        form = EditarContrasenaForm(request.POST)
        if form.is_valid():
            request.user.password = make_password(form.cleaned_data['password'])
            request.user.save()
            messages.success(request, 'La contraseña ha sido cambiado con exito!.')
            messages.success(request, 'Es necesario introducir los datos para entrar.')
            return redirect(reverse('accounts.index'))
    else:
        form = EditarContrasenaForm()
    return render(request, 'accounts/editar_contrasena.html', {'form': form})
