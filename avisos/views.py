from django.shortcuts import render, redirect, get_object_or_404
from .models import Aviso, AvisoAlumno
from usuarios.models import Alumno, Perfil, Apoderado
from curso.models import Curso
from django.contrib.auth.decorators import login_required
from .forms import AvisoForm, AvisoAlumnoForm
# seleccionar curso en caso de no venir desde uno. Administrador
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
# crear aviso. Administrador Profesor
@login_required
def crear_aviso(request, curso_id=None):
    perfil = request.user.perfil
    # si se viene desde un curso se seleccionara automaticamente
    if curso_id:
        curso_seleccionado = get_object_or_404(Curso, id=curso_id)
    # de lo contrario podra seleccionar un curso
    else:
        return redirect('avisos:seleccionar_curso') 
    alumnos = Alumno.objects.filter(curso=curso_seleccionado)  # Filtrar alumnos por el curso seleccionado
    if request.method == 'POST':
        aviso_form = AvisoForm(request.POST)
        # Verificar si se ha seleccionado todos los alumnos
        if 'seleccionar_todos' in request.POST:
            # Si se selecciona todos, tomamos todos los alumnos del curso
            selected_alumnos = alumnos
        else:
            # Si no, tomamos los seleccionados individualmente
            selected_alumnos = Alumno.objects.filter(id__in=request.POST.getlist('alumnos'))
        if aviso_form.is_valid():
            aviso = aviso_form.save(commit=False)
            aviso.creador = request.user.perfil  # Asignar el creador (perfil del usuario logueado)
            aviso.save()
            # Asignar los alumnos seleccionados al aviso
            for alumno in selected_alumnos:
                AvisoAlumno.objects.create(aviso=aviso, alumno=alumno)
             # Redirigir según el rol 
            if perfil.rol == 'administrador':
                return redirect('avisos:lista_avisos')  # Para administrador, redirigir a la lista general de avisos
            else:
                return redirect('avisos:mis_avisos')  # Para profesor, redirigir a su lista de avisos
    else:
        aviso_form = AvisoForm()  # Formulario de creación de aviso
    return render(request, 'avisos/crear_aviso.html', {
        'aviso_form': aviso_form,
        'alumnos': alumnos,  # Pasamos los alumnos filtrados por curso
        'curso_seleccionado': curso_seleccionado,  # Pasamos el curso seleccionado a la plantilla
    })
# lista de todos los avisos. Administrador
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
# detalle del aviso. profesor administrador
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
# editar aviso. profesor administrador
@login_required
def editar_aviso(request, aviso_id):
    aviso = get_object_or_404(Aviso, id=aviso_id)
    # Obtén el curso del primer alumno asociado al aviso
    alumno_asociado = AvisoAlumno.objects.filter(aviso=aviso).first()
    if alumno_asociado:
        curso_id = alumno_asociado.alumno.curso.id  # Obtener el curso del alumno
    else:
        curso_id = None  # Si no hay alumno asociado, no podemos obtener un curso
    if request.method == 'POST':
        aviso_form = AvisoForm(request.POST, instance=aviso)
        alumno_form = AvisoAlumnoForm(request.POST, curso_id=curso_id)
        if aviso_form.is_valid() and alumno_form.is_valid():
            aviso_form.save()  # Guarda los cambios del aviso
            # Verifica si se seleccionó el checkbox para todos los alumnos
            if alumno_form.cleaned_data['seleccionar_todos']:
                # Si se selecciona todos, tomamos todos los alumnos del curso
                selected_alumnos = alumno_form.fields['alumnos'].queryset
            else:
                # Si no, tomamos los seleccionados individualmente
                selected_alumnos = alumno_form.cleaned_data['alumnos']
            # Asigna los alumnos seleccionados
            AvisoAlumno.objects.filter(aviso=aviso).delete()  # Elimina los anteriores destinatarios
            for alumno in selected_alumnos:
                AvisoAlumno.objects.create(aviso=aviso, alumno=alumno)  # Asigna los nuevos destinatarios
            return redirect('avisos:detalle_aviso', aviso_id=aviso.id)  # Redirige a la misma página de detalle del aviso
    else:
        # Cargar los alumnos previamente asignados al aviso como "initial" para el formulario
        alumnos_asociados = AvisoAlumno.objects.filter(aviso=aviso).values_list('alumno', flat=True)
        aviso_form = AvisoForm(instance=aviso)
        alumno_form = AvisoAlumnoForm(initial={'alumnos': alumnos_asociados}, curso_id=curso_id)
    return render(request, 'avisos/editar_aviso.html', {
        'aviso': aviso,
        'aviso_form': aviso_form,
        'alumno_form': alumno_form
    })
# como se veran los avisos para los apoderados. Apoderado
@login_required
def avisos_apoderado(request):
    # Obtener la instancia de Apoderado asociada con el perfil del usuario actual
    perfil = request.user.perfil
    apoderado = get_object_or_404(Apoderado, perfil=perfil)
    # Obtener todos los alumnos bajo el cuidado de este apoderado
    alumnos = Alumno.objects.filter(apoderado=apoderado)
    # Obtener las notificaciones relacionadas con cada alumno
    avisos_por_alumno = {}
    for alumno in alumnos:
        avisos = AvisoAlumno.objects.filter(alumno=alumno).select_related('aviso')
        avisos_por_alumno[alumno] = avisos
    context = {
        'avisos_por_alumno': avisos_por_alumno
    }
    return render(request, 'avisos/avisos_apoderado.html', context)
# mostrar los avisos propios. Administrador Profesor
@login_required
def mis_avisos(request):
    # Filtrar los avisos creados por el usuario logueado
    avisos = Aviso.objects.filter(creador=request.user.perfil)
    for aviso in avisos:
        # Obtener los alumnos asociados al aviso
        alumnos = aviso.avisos_alumno.all()
        if alumnos.exists():  # Si existen alumnos asociados
            # Obtenemos el curso del primer alumno relacionado con este aviso
            curso = alumnos.first().alumno.curso
        else:
            curso = None
        aviso.curso = curso  # Agregar el curso al aviso para usarlo en la plantilla
    return render(request, 'avisos/mis_avisos.html', {'avisos': avisos})
# eliminar aviso. administrador
@login_required
def eliminar_aviso(request, aviso_id):
    aviso = get_object_or_404(Aviso, id=aviso_id)
    # Verificar si el usuario es el creador del aviso o un administrador
    if aviso.creador == request.user or request.user.perfil.rol == 'administrador':
        aviso.delete()
    else:
        return redirect('avisos:lista_avisos')
    return redirect('avisos:lista_avisos')