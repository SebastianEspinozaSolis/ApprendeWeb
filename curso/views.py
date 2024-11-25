from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso
from .forms import CursoForm
from django.contrib.auth.decorators import login_required
from asignatura.models import Asignatura
from evaluacion.models import Evaluacion
from usuarios.models import Profesor, Alumno, Apoderado
from jefatura.models import Jefatura
from django.contrib.auth.decorators import user_passes_test

def profesor_admin_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.perfil.rol == 'profesor' or request.user.perfil.rol == 'administrador':
            return function(request, *args, **kwargs)
        else:
            return redirect('curso:lista_cursos')
    return wrapper

@login_required
def lista_cursos(request):
    cursos = Curso.objects.all().order_by('-nombre')
    return render(request, 'curso/lista_cursos.html', {'cursos': cursos})

@login_required
def detalle_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    jefatura = Jefatura.objects.filter(curso=curso).first()
    asignaturas = curso.asignaturas.all()
    evaluaciones = Evaluacion.objects.filter(asignatura__curso=curso)
    profesores = Profesor.objects.filter(asignatura__curso=curso).distinct()
    alumnos = Alumno.objects.filter(curso=curso)
    apoderados = Apoderado.objects.filter(alumno__in=alumnos)
    return render(request, 'curso/detalle_curso.html', {
        'curso': curso,
        'jefatura': jefatura,
        'asignaturas': asignaturas,
        'evaluaciones': evaluaciones,
        'profesores': profesores,
        'alumnos': alumnos,
        'apoderados': apoderados,
    }
    )

@login_required
def crear_curso(request):
    if request.user.perfil.rol in ['profesor', 'administrador']:
        if request.method == 'POST':
            form = CursoForm(request.POST)
            if form.is_valid():
                curso = form.save(commit=False)
                curso.save()
                return redirect('curso:detalle_curso', pk=curso.pk)
        else:
            form = CursoForm()
        return render(request, 'curso/crear_curso.html', {'form': form})
    else:
        return redirect('curso:lista_cursos')

@login_required
def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.user.perfil.rol == 'administrador':
        if request.method == 'POST':
            form = CursoForm(request.POST, instance=curso)
            if form.is_valid():
                form.save()
                return redirect('curso:detalle_curso', pk=curso.pk)
        else:
            form = CursoForm(instance=curso)
        return render(request, 'curso/editar_curso.html', {'form': form})
    else:
        return redirect('curso:lista_cursos')

@profesor_admin_required
def ver_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    return render(request, 'curso/ver_curso.html', {'curso': curso})
    
    
@profesor_admin_required
def gestionar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    return render(request, 'curso/gestionar_curso.html', {'curso': curso})
        
