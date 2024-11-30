from django.shortcuts import render, redirect, get_object_or_404
from .models import Asignatura
from .forms import AsignaturaForm
from django.contrib.auth.decorators import login_required
from curso.models import Curso
from evaluacion.models import Evaluacion
from usuarios.models import Alumno
# lista de asignaturas por un curso. Todos los usuarios
@login_required
def lista_asignaturas(request, curso_id=None):
    asignaturas = Asignatura.objects.all().order_by('-nombre')
    curso = None  # Variable para el curso específico
    if curso_id:
        curso = get_object_or_404(Curso, pk=curso_id)  # Obtén el curso específico
        asignaturas = asignaturas.filter(curso=curso)  # Filtra las asignaturas por curso
    return render(request, 'asignatura/lista_asignaturas.html', {
        'asignaturas': asignaturas,
        'curso': curso,
    })
# detalle de una de las asignatura. Administrador y profesor que realiza la asignatura
@login_required
def detalle_asignatura(request, pk):
    asignatura = get_object_or_404(Asignatura, pk=pk)
    curso = asignatura.curso  # Obtener el curso de la asignatura
    evaluaciones = Evaluacion.objects.filter(asignatura=asignatura)  # Obtener evaluaciones de la asignatura
    alumno = None
    return render(request, 'asignatura/detalle_asignatura.html', {
        'asignatura': asignatura,
        'curso': curso,
        'evaluaciones': evaluaciones,
        'alumno': alumno,  # Pasamos el alumno al contexto
    })
# crear asignatura. Administrador
@login_required
def crear_asignatura(request, curso_id=None):
    curso = None
    if curso_id:
        curso = get_object_or_404(Curso, pk=curso_id)
    if request.user.perfil.rol in ['profesor', 'administrador']:
        if request.method == 'POST':
            form = AsignaturaForm(request.POST)
            if form.is_valid():
                asignatura = form.save(commit=False)
                if curso:
                    asignatura.curso = curso
                asignatura.save()
                return redirect('asignatura:detalle_asignatura', pk=asignatura.pk)
        else:
            form = AsignaturaForm(initial={'curso': curso} if curso else {})
        return render(request, 'asignatura/crear_asignatura.html', {'form': form, 'curso': curso})
    else:
        return redirect('asignatura:lista_asignaturas')
#editar asignatura. Administrador
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