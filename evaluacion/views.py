from django.shortcuts import render, redirect, get_object_or_404
from .models import Evaluacion
from .forms import EvaluacionForm
from django.contrib.auth.decorators import login_required

@login_required
def lista_evaluaciones(request):
    evaluaciones = Evaluacion.objects.all().order_by('-fecha')
    return render(request, 'evaluacion/lista_evaluaciones.html', {'evaluaciones': evaluaciones})
@login_required
def detalle_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    return render(request, 'evaluacion/detalle_evaluacion.html', {'evaluacion': evaluacion})

@login_required
def crear_evaluacion(request):
    if request.user.perfil.rol in ['profesor', 'administrador']:
        if request.method == 'POST':
            form = EvaluacionForm(request.POST)
            if form.is_valid():
                evaluacion = form.save(commit=False)
                evaluacion.save()
                return redirect('evaluacion:detalle_evaluacion', pk=evaluacion.pk)
        else:
            form = EvaluacionForm()
        return render(request, 'evaluacion/crear_evaluacion.html', {'form': form})
    else:
        return redirect('evaluacion:lista_evaluaciones')

@login_required
def editar_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    if request.user.perfil.rol == 'administrador':
        if request.method == 'POST':
            form = EvaluacionForm(request.POST, instance=evaluacion)
            if form.is_valid():
                form.save()
                return redirect('evaluacion:detalle_evaluacion', pk=evaluacion.pk)
        else:
            form = EvaluacionForm(instance=evaluacion)
        return render(request, 'evaluacion/editar_evaluacion.html', {'form': form})
    else:
        return redirect('evaluacion:lista_evaluaciones')