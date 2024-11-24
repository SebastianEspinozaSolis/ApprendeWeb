from django.shortcuts import render, get_object_or_404, redirect
from .models import Justificativo
from asistencia.models import Asistencia
from .forms import JustificativoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def justificar_asistencia(request, asistencia_id):
    # Obtener la asistencia para la cual se creará el justificativo
    asistencia = get_object_or_404(Asistencia, id=asistencia_id)

    # Verificar que la asistencia esté ausente para permitir la justificación
    if asistencia.asistio:
        return redirect('asistencia:detalle_asistencia', asignatura_id=asistencia.asignatura.id, alumno_id=asistencia.alumno.id)

    # Verificar si ya existe un justificativo para la fecha y alumno
    if Justificativo.objects.filter(alumno=asistencia.alumno, fecha=asistencia.fecha).exists():
        messages.warning(request, "Ya existe un justificativo para esta fecha.")
        return redirect('asistencia:detalle_asistencia', asignatura_id=asistencia.asignatura.id, alumno_id=asistencia.alumno.id)

    if request.method == 'POST':
        form = JustificativoForm(request.POST)
        if form.is_valid():
            # Crear justificativo
            justificativo = form.save(commit=False)
            justificativo.alumno = asistencia.alumno
            justificativo.fecha = asistencia.fecha
            justificativo.save()

            # No actualizar la asistencia aquí (se hará solo al aprobar)
            messages.success(request, "El justificativo ha sido creado correctamente y está pendiente de aprobación.")
            return redirect('asistencia:detalle_asistencia', asignatura_id=asistencia.asignatura.id, alumno_id=asistencia.alumno.id)
    else:
        form = JustificativoForm()

    return render(request, 'justificativo/justificar_asistencia.html', {'form': form, 'asistencia': asistencia})



@login_required
def gestionar_justificativos(request):
    justificativos = Justificativo.objects.filter(estado='pendiente')

    if 'accion' in request.GET and 'justificativo_id' in request.GET:
        justificativo_id = request.GET['justificativo_id']
        accion = request.GET['accion']
        justificativo = get_object_or_404(Justificativo, id=justificativo_id)

        if accion == 'aprobar':
            justificativo.estado = 'aprobado'
            justificativo.save()

            # Aplicar el justificativo a todas las asistencias del mismo día
            asistencias = Asistencia.objects.filter(alumno=justificativo.alumno, fecha=justificativo.fecha)
            if asistencias.exists():
                for asistencia in asistencias:
                    if not asistencia.asistio:  # Si no asistió, marcar como asistido
                        asistencia.asistio = True
                        asistencia.save()
            else:
                print("No se encontraron asistencias para este alumno en esa fecha.")

        elif accion == 'rechazar':
            justificativo.estado = 'rechazado'
            justificativo.save()

        return redirect('justificativo:gestionar_justificativos')

    return render(request, 'justificativo/gestionar_justificativos.html', {'justificativos': justificativos})
