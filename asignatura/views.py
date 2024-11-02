from django.shortcuts import render, redirect, get_object_or_404
from .models import Asignatura
from .forms import AsignaturaForm
from django.contrib.auth.decorators import login_required

@login_required
def lista_asignaturas(request):
    asignaturas = Asignatura.objects.all().order_by('-nombre')
    return render(request, 'asignatura/lista_asignaturas.html', {'asignaturas': asignaturas})
@login_required
def detalle_asignatura(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    return render(request, 'asignatura/detalle_asignatura.html', {'asignatura': asignatura})

@login_required
def crear_asignatura(request):
    if request.user.perfil.rol in ['profesor', 'administrador']:
        if request.method == 'POST':
            form = AsignaturaForm(request.POST)
            if form.is_valid():
                asignatura = form.save(commit=False)
                asignatura.save()
                return redirect('asignatura:detalle_asignatura', pk=asignatura.pk)
        else:
            form = AsignaturaForm()
        return render(request, 'asignatura/crear_asignatura.html', {'form': form})
    else:
        return redirect('asignatura:lista_asignaturas')

@login_required
def editar_asignatura(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    if request.user.perfil.rol == 'administrador':
        if request.method == 'POST':
            form = AsignaturaForm(request.POST, instance=asignatura)
            if form.is_valid():
                form.save()
                return redirect('asignatura:detalle_asignatura', pk=asignatura.pk)
        else:
            form = AsignaturaForm(instance=asignatura)
        return render(request, 'asignatura/editar_asignatura.html', {'form': form})
    else:
        return redirect('asignatura:lista_asignatura')