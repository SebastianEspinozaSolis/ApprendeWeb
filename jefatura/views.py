from django.shortcuts import render, redirect, get_object_or_404
from .models import Jefatura
from .forms import JefaturaForm
from django.contrib.auth.decorators import login_required
from curso.models import Curso
# opcion de crear una jefatura. Administrador
@login_required
def crear_jefatura(request):
    if request.method == 'POST':
        form = JefaturaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('jefatura:lista_jefaturas')  # Redirige a la lista de jefaturas
    else:
        curso_id = request.GET.get('curso_id')  # Obtener el curso_id de la URL en caso de venir desde un curso
        initial_data = {}
        if curso_id:
            curso = get_object_or_404(Curso, pk=curso_id)
            initial_data['curso'] = curso
        form = JefaturaForm(initial=initial_data)
    return render(request, 'jefatura/crear_jefatura.html', {'form': form})
# lista de jefaturas y cursos. Administrador
@login_required
def lista_jefaturas(request):
    jefaturas = Jefatura.objects.all().select_related('curso', 'profesor')  # Optimizamos la consulta
    return render(request, 'jefatura/lista_jefaturas.html', {
        'jefaturas': jefaturas,
    })
# editar jefatura. Administrador
@login_required
def editar_jefatura(request, pk):
    jefatura = get_object_or_404(Jefatura, pk=pk)
    if request.method == 'POST':
        form = JefaturaForm(request.POST, instance=jefatura)
        if form.is_valid():
            jefatura = form.save()
            # Verificar si hay un ID de curso en la solicitud
            curso_id = request.POST.get('curso_id')  # Asegúrate de que el campo curso_id esté en tu formulario
            if curso_id:
                return redirect('curso:detalle_curso', pk=curso_id)
            else:
                return redirect('jefatura:lista_jefaturas')
    else:
        form = JefaturaForm(instance=jefatura)
    return render(request, 'jefatura/editar_jefatura.html', {'form': form})
