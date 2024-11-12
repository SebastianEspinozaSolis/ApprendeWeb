# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Aviso, AvisoAlumno
from usuarios.models import Alumno, Perfil
from curso.models import Curso
from django.contrib.auth.decorators import login_required
from .forms import AvisoForm, AvisoAlumnoForm

@login_required
def seleccionar_curso(request):
    if request.user.perfil.rol == 'administrador':  # Solo el admin puede seleccionar curso
        cursos = Curso.objects.all()  # Obtener todos los cursos
        if request.method == 'POST':
            curso_seleccionado = request.POST.get('curso')
            return redirect('avisos:crear_aviso', curso_id=curso_seleccionado)  # Redirigir con el curso seleccionado
        return render(request, 'avisos/seleccionar_curso.html', {'cursos': cursos})
    
    else:
        # Si es profesor, redirigir a la creación de aviso con su curso asignado
        perfil = request.user.perfil
        if perfil.rol == 'profesor' and perfil.jefatura:
            return redirect('avisos:crear_aviso', curso_id=perfil.jefatura.id)
        return redirect('avisos:crear_aviso')
# views.py
@login_required
def crear_aviso(request, curso_id=None):
    if request.user.perfil.rol == 'profesor':
        # El curso del profesor ya está asignado por su jefatura
        curso_seleccionado = request.user.perfil.jefatura
    elif curso_id:
        curso_seleccionado = Curso.objects.get(id=curso_id)
    else:
        return redirect('avisos:seleccionar_curso')  # Redirigir si no se pasa curso

    cursos = Curso.objects.all()
    alumnos = Alumno.objects.filter(curso=curso_seleccionado)  # Filtrar alumnos por el curso seleccionado

    if request.method == 'POST':
        aviso_form = AvisoForm(request.POST)
        alumno_form = AvisoAlumnoForm(request.POST)

        if aviso_form.is_valid() and alumno_form.is_valid():
            aviso = aviso_form.save(commit=False)
            aviso.creador = request.user.perfil  # Asignar el creador (perfil del usuario logueado)
            aviso.save()

            # Asignar los alumnos seleccionados al aviso
            for alumno in alumno_form.cleaned_data['alumnos']:
                AvisoAlumno.objects.create(aviso=aviso, alumno=alumno)

            # Redirigir a la lista de avisos
            return redirect('avisos:lista_avisos')

    else:
        aviso_form = AvisoForm()  # Formulario de creación de aviso
        alumno_form = AvisoAlumnoForm()  # Formulario de selección de alumnos

    return render(request, 'avisos/crear_aviso.html', {
        'aviso_form': aviso_form,
        'alumno_form': alumno_form,
        'cursos': cursos,  # Pasamos los cursos para el filtro
        'alumnos': alumnos,  # Pasamos los alumnos filtrados por curso
        'curso_seleccionado': curso_seleccionado,  # Pasamos el curso seleccionado a la plantilla
    })
@login_required
def lista_avisos(request):
    avisos = Aviso.objects.all()  # Obtener todos los avisos

    for aviso in avisos:
        # Obtener los alumnos asociados al aviso
        alumnos = aviso.avisos_alumno.all()

        if alumnos.exists():  # Si existen alumnos asociados
            # Obtenemos el curso del primer alumno relacionado con este aviso
            curso = alumnos.first().alumno.curso
        else:
            curso = None

        aviso.curso = curso  # Agregar el curso al aviso para usarlo en la plantilla
    
    return render(request, 'avisos/lista_avisos.html', {'avisos': avisos})

@login_required
def detalle_aviso(request, aviso_id):
    # Obtener el aviso específico
    aviso = get_object_or_404(Aviso, pk=aviso_id)
    
    # Obtener los alumnos a los que se envió el aviso a través del modelo AvisoAlumno
    alumnos_notificados = AvisoAlumno.objects.filter(aviso=aviso).values_list('alumno', flat=True)
    
    # Obtener los objetos Alumno correspondientes
    alumnos = Alumno.objects.filter(id__in=alumnos_notificados)

    return render(request, 'avisos/detalle_aviso.html', {
        'aviso': aviso,
        'alumnos_notificados': alumnos
    })

def detalle_aviso(request, aviso_id):
    aviso = get_object_or_404(Aviso, id=aviso_id)
    
    if request.method == 'POST':
        aviso_form = AvisoForm(request.POST, instance=aviso)
        alumno_form = AvisoAlumnoForm(request.POST)

        if aviso_form.is_valid() and alumno_form.is_valid():
            aviso_form.save()  # Guarda los cambios del aviso
            # Asignar los alumnos seleccionados
            selected_alumnos = alumno_form.cleaned_data['alumnos']
            AvisoAlumno.objects.filter(aviso=aviso).delete()  # Elimina los anteriores destinatarios
            for alumno in selected_alumnos:
                AvisoAlumno.objects.create(aviso=aviso, alumno=alumno)  # Asigna los nuevos destinatarios
            return redirect('avisos:detalle_aviso', aviso_id=aviso.id)  # Redirige a la misma página con los cambios

    else:
        aviso_form = AvisoForm(instance=aviso)
        alumno_form = AvisoAlumnoForm()

    return render(request, 'avisos/detalle_aviso.html', {
        'aviso': aviso,
        'aviso_form': aviso_form,
        'alumno_form': alumno_form
    })
def editar_aviso(request, aviso_id):
    aviso = get_object_or_404(Aviso, id=aviso_id)
    
    if request.method == 'POST':
        aviso_form = AvisoForm(request.POST, instance=aviso)
        alumno_form = AvisoAlumnoForm(request.POST)

        if aviso_form.is_valid() and alumno_form.is_valid():
            aviso_form.save()  # Guarda los cambios del aviso
            # Asignar los alumnos seleccionados
            selected_alumnos = alumno_form.cleaned_data['alumnos']
            AvisoAlumno.objects.filter(aviso=aviso).delete()  # Elimina los anteriores destinatarios
            for alumno in selected_alumnos:
                AvisoAlumno.objects.create(aviso=aviso, alumno=alumno)  # Asigna los nuevos destinatarios
            return redirect('avisos:detalle_aviso', aviso_id=aviso.id)  # Redirige a la misma página de detalle del aviso

    else:
        aviso_form = AvisoForm(instance=aviso)
        alumno_form = AvisoAlumnoForm()

    return render(request, 'avisos/editar_aviso.html', {
        'aviso': aviso,
        'aviso_form': aviso_form,
        'alumno_form': alumno_form
    })