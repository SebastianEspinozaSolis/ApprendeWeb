from django.shortcuts import render, redirect, get_object_or_404
from .models import Calificacion
from .forms import CalificacionForm, EditarCalificacionForm
from django.contrib.auth.decorators import login_required
from evaluacion.models import Evaluacion
from usuarios.models import Alumno
from usuarios.decorators import profesor_admin_required

@login_required
@profesor_admin_required
def crear_calificacion(request):
    evaluacion = None
    evaluacion_id = request.GET.get('evaluacion_id')  # Obtener el ID de la evaluación desde los parámetros GET
    if evaluacion_id:
        evaluacion = get_object_or_404(Evaluacion, pk=evaluacion_id)  # Obtener la evaluación específica
    
    if request.user.perfil.rol in ['profesor', 'administrador']:
        alumnos = Alumno.objects.filter(curso=evaluacion.asignatura.curso) if evaluacion else []

        if request.method == 'POST':
            for alumno in alumnos:
                calificacion_value = request.POST.get(f'calificacion_{alumno.id}')
                if calificacion_value:  # Crear una calificación solo si el valor fue ingresado
                    Calificacion.objects.create(
                        calificacion=calificacion_value,
                        alumno=alumno,
                        evaluacion=evaluacion
                    )
            return redirect('evaluacion:detalle_evaluacion', pk=evaluacion_id)

        return render(request, 'calificacion/crear_calificacion.html', {
            'evaluacion': evaluacion,
            'alumnos': alumnos,
        })
    else:
        return redirect('evaluacion:detalle_evaluacion', pk=evaluacion_id)
@login_required
@profesor_admin_required
def editar_calificacion(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    if request.method == 'POST':
        form = EditarCalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()
            # Redirect to the evaluation detail view after saving the grade
            return redirect('evaluacion:detalle_evaluacion', pk=calificacion.evaluacion.pk)
    else:
        form = EditarCalificacionForm(instance=calificacion)
    
    return render(request, 'calificacion/editar_calificacion.html', {
        'form': form,
        'calificacion': calificacion
    })