from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from inicio.forms import UserForm
from inicio.models import UserProfile, Cita
import inicio.views as traer

@login_required(login_url='acceso_denegado')
def signout(request):
    logout(request)
    return redirect('loginregister')

@login_required(login_url='acceso_denegado')
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

@login_required(login_url='acceso_denegado')
def configuracion(request, id):
    perfil_usuario = UserProfile.objects.get(id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserForm(instance=perfil_usuario)
    return render(request, 'configuracion.html', {'form': form})

@login_required(login_url='acceso_denegado')
def correo(request):
    return render(request, 'correo.html')

@login_required(login_url='acceso_denegado')
def calendario(request):
    if request.user.is_superuser:
        # Si es superusuario, obtener todas las citas programadas
        citas = Cita.objects.filter(estado='programada')
    else:
        # Si es un paciente normal, obtener solo sus citas programadas
        citas = Cita.objects.filter(paciente=request.user, estado='programada')
    
    return render(request, 'calendario.html', {'citas': citas})
