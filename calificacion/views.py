from django.shortcuts import render, redirect, get_object_or_404
from .models import Calificacion
from .forms import CalificacionForm
from django.contrib.auth.decorators import login_required

@login_required
def lista_calificaciones(request):
    calificaciones = Calificacion.objects.all().order_by('-calificacion')
    return render(request, 'calificacion/lista_calificaciones.html', {'calificaciones': calificaciones})
@login_required
def detalle_calificacion(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    return render(request, 'calificacion/detalle_calificacion.html', {'calificacion': calificacion})

@login_required
def crear_calificacion(request):
    if request.user.perfil.rol in ['profesor', 'administrador']:
        if request.method == 'POST':
            form = CalificacionForm(request.POST)
            if form.is_valid():
                calificacion = form.save(commit=False)
                calificacion.save()
                return redirect('calificacion:detalle_calificacion', pk=calificacion.pk)
        else:
            form = CalificacionForm()
        return render(request, 'calificacion/crear_calificacion.html', {'form': form})
    else:
        return redirect('calificacion:lista_calificaciones')

@login_required
def editar_calificacion(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    if request.user.perfil.rol == 'administrador':
        if request.method == 'POST':
            form = CalificacionForm(request.POST, instance=calificacion)
            if form.is_valid():
                form.save()
                return redirect('calificacion:detalle_calificacion', pk=calificacion.pk)
        else:
            form = CalificacionForm(instance=calificacion)
        return render(request, 'calificacion/editar_calificacion.html', {'form': form})
    else:
        return redirect('calificacion:lista_calificacion')