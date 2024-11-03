from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso
from .forms import CursoForm
from django.contrib.auth.decorators import login_required
from asignatura.models import Asignatura
from evaluacion.models import Evaluacion

@login_required
def lista_cursos(request):
    cursos = Curso.objects.all().order_by('-nombre')
    return render(request, 'curso/lista_cursos.html', {'cursos': cursos})
@login_required
def detalle_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    asignaturas = Asignatura.objects.filter(curso=curso).select_related('curso')
    evaluaciones = Evaluacion.objects.filter(asignatura__curso=curso).order_by('fecha')  # Obtener evaluaciones relacionadas al curso
    return render(request, 'curso/detalle_curso.html', {
        'curso': curso,
        'asignaturas': asignaturas,
        'evaluaciones': evaluaciones,  # Pasar evaluaciones al contexto
    })

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