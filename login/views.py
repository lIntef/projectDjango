from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db import IntegrityError
from .models import UserProfile

def registrarme(request):
    error_message = None
    success_message = None

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 and password2:
            if password1 == password2:
                try:
                    # Verificar si ya existe un usuario con el mismo número de documento
                    existing_user = UserProfile.objects.get(numero=request.POST['numero'])
                    error_message = 'El número de documento ya está en uso'
                except UserProfile.DoesNotExist:
                    try:
                        user = UserProfile.objects.create(
                            tipo=request.POST['type'],
                            numero=request.POST['numero'],
                            username=request.POST['username'],
                            email=request.POST['email'],
                            password=password1
                        )
                        user.set_password(password1)
                        user.save()
                        success_message = 'Cuenta Creada Correctamente, Por favor inicie sesión'
                    except IntegrityError as e:
                        if 'unique constraint' in str(e):
                            error_message = 'El usuario ya fue creado'
                        else:
                            error_message = f'Error al crear el usuario: {e}'
            else:
                error_message = 'Las contraseñas no coinciden'
        else:
            error_message = None

            if request.method == 'POST':
                numero = request.POST.get('numer')
                password = request.POST.get('contra')
                print(numero)
                print(password)    
                #user = UserProfile.objects.get(numero=numero, password=password)
                user = authenticate(request, username=numero, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboardDoc')
                else:
                    error_message = 'Credenciales inválidas'

            context = {
                'error': error_message,
            }
            return render(request, 'loginregister.html', context)

    context = {
        'error': error_message,
        'done': success_message
    }
    return render(request, 'loginregister.html', context)

# ... (el resto de tus vistas)


def loginregister(request):
    return render(request, 'loginregister.html')

def inicio(request):
    return render(request, 'inicio.html')

def signout(request):
    logout(request)
    return redirect('loginregister')

def dashboardDoc(request):
    return render(request, 'dashboardDoc.html')

def configuracion(request):
    return render(request, 'configuracion.html')

def editaraccount(request):
    return render(request, 'editaraccount.html')

def correo(request):
    return render(request, 'correo.html')

def calendario(request):
    return render(request, 'calendario.html')

def agendarcita(request):
    return render(request, 'agendarcita.html')

def editarcita(request):
    return render(request, 'editarcitas.html')

def newhistoriaclinica(request):
    return render(request, 'newhistoriaclinica.html')

def historias(request):
    return render(request, 'historias.html')

def agregarfechas(request):
    return render(request, 'agregarfechas.html')
