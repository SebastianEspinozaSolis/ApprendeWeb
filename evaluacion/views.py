from django.shortcuts import render, redirect, get_object_or_404
from .models import Evaluacion
from .forms import EvaluacionForm
from django.contrib.auth.decorators import login_required
from asignatura.models import Asignatura

@login_required
def lista_evaluaciones(request, asignatura_id=None):
    evaluaciones = Evaluacion.objects.all().order_by('-fecha')
    if asignatura_id:
        evaluaciones = evaluaciones.filter(asignatura__id=asignatura_id)  # Filtrar por asignatura
    return render(request, 'evaluacion/lista_evaluaciones.html', {'evaluaciones': evaluaciones})

@login_required
def detalle_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    asignatura = evaluacion.asignatura  # Obtener la asignatura relacionada
    curso = evaluacion.asignatura.curso
    return render(request, 'evaluacion/detalle_evaluacion.html', {
        'evaluacion': evaluacion,
        'asignatura': asignatura,  
        'curso':curso,
    })

@login_required
def crear_evaluacion(request):
    asignatura = None
    asignatura_id = request.GET.get('asignatura_id')  # Obtener la asignatura_id de los parámetros GET
    if asignatura_id:
        asignatura = get_object_or_404(Asignatura, pk=asignatura_id)  # Obtener la asignatura específica
    if request.user.perfil.rol in ['profesor', 'administrador']:
        if request.method == 'POST':
            form = EvaluacionForm(request.POST)
            if form.is_valid():
                evaluacion = form.save(commit=False)
                if asignatura:
                    evaluacion.asignatura = asignatura  # Asignar la asignatura
                evaluacion.save()
                return redirect('evaluacion:detalle_evaluacion', pk=evaluacion.pk)
        else:
            form = EvaluacionForm(initial={'asignatura': asignatura})  # Inicializar el formulario con la asignatura, si está presente
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