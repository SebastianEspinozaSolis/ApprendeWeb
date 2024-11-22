from django.shortcuts import render, redirect, get_object_or_404
from .models import Asistencia
from .forms import AsistenciaForm, EditarAsistenciaForm
from django.contrib.auth.decorators import login_required
from asignatura.models import Asignatura, Curso
from usuarios.models import Alumno
from django.db.models import Count, Case, When, IntegerField
from django.forms import modelformset_factory
from django.contrib import messages
from usuarios.decorators import profesor_admin_required

@login_required
@profesor_admin_required
def crear_asistencia(request, asignatura_id):  # Recibe asignatura_id desde la URL
    asignatura = get_object_or_404(Asignatura, pk=asignatura_id)  # Obtener la asignatura específica
    
    if request.user.perfil.rol in ['profesor', 'administrador']:
        alumnos = Alumno.objects.filter(curso__in=[asignatura.curso]) if asignatura else []

        if request.method == 'POST':
            fecha = request.POST.get('fecha')
            for alumno in alumnos:
                # Aquí se verifica si el checkbox de asistencia para este alumno está marcado
                asistio_value = request.POST.get(f'asistio_{alumno.id}')
                if asistio_value:  # El valor "on" se enviará si el checkbox está marcado
                    Asistencia.objects.create(
                        asistio=True,  # Asistió si el checkbox está marcado
                        alumno=alumno,
                        asignatura=asignatura,
                        fecha=fecha
                    )
                else:
                    # Si no está marcado, la asistencia es "False"
                    Asistencia.objects.create(
                        asistio=False,  # No asistió si el checkbox no está marcado
                        alumno=alumno,
                        asignatura=asignatura,
                        fecha=fecha
                    )
            return redirect('asistencia:lista_fechas_asistencia', asignatura_id=asignatura_id)

        return render(request, 'asistencia/crear_asistencia.html', {
            'asignatura': asignatura,
            'alumnos': alumnos,
            'fecha': request.GET.get('fecha'),  # Pasar la fecha seleccionada
        })
    else:
        return redirect('asistencia:lista_fechas_asistencia', asignatura_id=asignatura_id)

@login_required
@profesor_admin_required
def editar_asistencia(request, asistencia_id):
    asistencia_inicial = get_object_or_404(Asistencia, pk=asistencia_id)
    asignatura = asistencia_inicial.asignatura
    fecha = asistencia_inicial.fecha
    
    # Crear formset para todas las asistencias de la misma fecha y asignatura
    AsistenciaFormSet = modelformset_factory(
        Asistencia, 
        fields=('asistio', 'justificacion'),
        extra=0
    )
    
    # Obtener todas las asistencias de la misma fecha y asignatura
    queryset = Asistencia.objects.filter(
        asignatura=asignatura,
        fecha=fecha
    ).select_related('alumno')

    if request.method == 'POST':
        formset = AsistenciaFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Asistencias actualizadas correctamente.')
            return redirect('asistencia:lista_fechas_asistencia', asignatura_id=asignatura.id)
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        formset = AsistenciaFormSet(queryset=queryset)

    context = {
        'formset': formset,
        'asignatura': asignatura,
        'fecha': fecha,
    }
    
    return render(request, 'asistencia/editar_asistencia.html', context)

@login_required
@profesor_admin_required
def lista_fechas_asistencia(request, asignatura_id):
    asignatura = get_object_or_404(Asignatura, id=asignatura_id)
    fecha_filtro = request.GET.get('fecha')
    
    # Obtener asistencias
    asistencias = Asistencia.objects.filter(asignatura_id=asignatura_id)
    if fecha_filtro:
        asistencias = asistencias.filter(fecha=fecha_filtro)
    
    # Contar presentes y ausentes (sin duplicar por fecha)
    total_presentes = asistencias.filter(asistio=True).count()
    total_ausentes = asistencias.filter(asistio=False).count()
    total = total_presentes + total_ausentes
    
    # Calcular porcentajes
    if total > 0:
        porcentaje_presentes = (total_presentes / total) * 100
        porcentaje_ausentes = (total_ausentes / total) * 100
    else:
        porcentaje_presentes = 0
        porcentaje_ausentes = 0
    
    # Organizar asistencias por fecha
    asistencias_por_fecha = {}
    for asistencia in asistencias:
        fecha = asistencia.fecha
        if fecha not in asistencias_por_fecha:
            asistencias_por_fecha[fecha] = []
        asistencias_por_fecha[fecha].append(asistencia)

    context = {
        'asignatura': asignatura,
        'asistencias_por_fecha': asistencias_por_fecha,
        'fecha_filtro': fecha_filtro,
        'porcentaje_presentes': porcentaje_presentes,
        'porcentaje_ausentes': porcentaje_ausentes,
        'total_presentes': total_presentes,
        'total_ausentes': total_ausentes
    }
    
    return render(request, 'asistencia/lista_fechas_asistencia.html', context)

@login_required
@profesor_admin_required
def actualizar_asistencia(request, asistencia_id):
    asistencia = get_object_or_404(Asistencia, pk=asistencia_id)
    
    if request.method == 'POST':
        asistio = request.POST.get('asistio') == 'true'
        asistencia.asistio = asistio
        asistencia.save()
        
        # Obtener la URL de retorno
        return redirect('asistencia:lista_fechas_asistencia', asignatura_id=asistencia.asignatura.id)
    
    # Si no es POST, redirigir a la lista de asistencias
    return redirect('asistencia:lista_fechas_asistencia', asignatura_id=asistencia.asignatura.id)

@login_required
@profesor_admin_required
def detalle_asistencia(request, asignatura_id, alumno_id):
    asignatura = get_object_or_404(Asignatura, pk=asignatura_id)
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    
    # Obtener todas las asistencias del alumno en la asignatura
    asistencias = Asistencia.objects.filter(alumno=alumno, asignatura=asignatura)
    
    # Contar el total de clases y las veces que asistió
    total_clases = asistencias.count()
    clases_asistidas = asistencias.filter(asistio=True).count()

    # Calcular el porcentaje de asistencia
    if total_clases > 0:
        porcentaje_asistencia = (clases_asistidas / total_clases) * 100
    else:
        porcentaje_asistencia = 0

    return render(request, 'asistencia/detalle_asistencia.html', {
        'asignatura': asignatura,
        'alumno': alumno,
        'asistencias': asistencias,
        'porcentaje_asistencia': porcentaje_asistencia,
    })

@login_required
def lista_cursos(request):  # o el nombre de tu vista actual
    if request.user.perfil.rol == 'administrador':
        cursos = Curso.objects.all()  # El admin ve todos los cursos
    elif request.user.perfil.rol == 'profesor':
        cursos = Curso.objects.filter(profesor=request.user)
    else:
        cursos = Curso.objects.filter(estudiantes=request.user)
    
    return render(request, 'curso/lista_cursos.html', {'cursos': cursos})
    