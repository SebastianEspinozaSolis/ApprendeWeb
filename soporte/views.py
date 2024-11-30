from django.shortcuts import render, redirect
from .forms import ReporteForm
from django.contrib.auth.decorators import login_required
# creacion de reporte de bug, sugerencia. todo usuario autentificado
@login_required
def crear_reporte(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = request.user  # Asigna el usuario actual al campo 'usuario'
            reporte.save()
            if request.user.perfil.rol == 'administrador':
                return redirect('usuarios:menu_administrador')  
            elif request.user.perfil.rol == 'profesor':
                return redirect('usuarios:menu_profesor') 
            elif request.user.perfil.rol == 'alumno':
                return redirect('usuarios:menu_alumno')  
            elif request.user.perfil.rol == 'apoderado':
                return redirect('usuarios:menu_apoderado')
    else:
        form = ReporteForm()

    return render(request, 'soporte/crear_reporte.html', {'form': form})
