from django.shortcuts import render, redirect, get_object_or_404
from .models import Asistencia
from .forms import AsistenciaForm, EditarAsistenciaForm
from django.contrib.auth.decorators import login_required
from asignatura.models import Asignatura
from usuarios.models import Alumno
from django.db.models import Count, Q

@login_required
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
def editar_asistencia(request, pk):
    asistencia = get_object_or_404(Asistencia, pk=pk)
    if request.method == 'POST':
        form = EditarAsistenciaForm(request.POST, instance=asistencia)
        if form.is_valid():
            form.save()
            # Redirigir a la vista de detalles de la asignatura después de guardar
            return redirect('asistencia:lista_fechas_asistencia', asignatura_id=asistencia.asignatura.id)
    else:
        form = EditarAsistenciaForm(instance=asistencia)
    
    return render(request, 'asistencia/editar_asistencia.html', {
        'form': form,
        'asistencia': asistencia
    })

@login_required
def lista_fechas_asistencia(request, asignatura_id):
    asignatura = get_object_or_404(Asignatura, id=asignatura_id)

    # Obtener la fecha de filtro desde los parámetros de la URL
    fecha_filtro = request.GET.get('fecha')  # Obtener la fecha seleccionada por el usuario

    # Filtrar las asistencias por fecha si se especifica, de lo contrario obtener todas las asistencias
    if fecha_filtro:
        asistencias = Asistencia.objects.filter(asignatura=asignatura, fecha=fecha_filtro).order_by('fecha')
    else:
        asistencias = Asistencia.objects.filter(asignatura=asignatura).order_by('fecha')

    # Agrupar las asistencias por fecha
    asistencias_por_fecha = {}
    for asistencia in asistencias:
        if asistencia.fecha not in asistencias_por_fecha:
            asistencias_por_fecha[asistencia.fecha] = []
        asistencias_por_fecha[asistencia.fecha].append(asistencia)

    return render(request, 'asistencia/lista_fechas_asistencia.html', {
        'asignatura': asignatura,
        'asistencias_por_fecha': asistencias_por_fecha,
        'fecha_filtro': fecha_filtro,  # Pasar la fecha al template
    })


@login_required
def detalle_asistencia(request, asignatura_id, alumno_id):
    asignatura = get_object_or_404(Asignatura, pk=asignatura_id)
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    
    # Filtrar las asistencias para ese alumno en esa asignatura específica
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
def menu_asignaturas_apoderado(request, alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    asignaturas = Asignatura.objects.filter(curso=alumno.curso)

    data_asistencias = asignaturas.annotate(
        total_clases=Count('asistencia', filter=Q(asistencia__alumno=alumno)),
        clases_asistidas=Count('asistencia', filter=Q(asistencia__alumno=alumno, asistencia__asistio=True))
    ).values('id', 'nombre', 'total_clases', 'clases_asistidas')

    # Crear una lista de datos con el nombre y porcentaje de asistencia
    asignaturas_con_datos = []
    for asignatura in data_asistencias:
        total = asignatura['total_clases']
        asistidas = asignatura['clases_asistidas']
        porcentaje_asistencia = (asistidas / total) * 100 if total > 0 else 0

        # Añadir el nombre y el porcentaje de asistencia al diccionario
        asignaturas_con_datos.append({
            'id': asignatura['id'],
            'nombre': asignatura['nombre'],
            'porcentaje_asistencia': porcentaje_asistencia
        })

    return render(request, 'asistencia/menu_asignaturas_apoderado.html', {
        'alumno': alumno,
        'asignaturas_con_datos': asignaturas_con_datos,
    })
