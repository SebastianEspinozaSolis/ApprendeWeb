from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AjustesForm
from .models import Ajustes

@login_required
def ajustes(request):
    # Obtener o crear ajustes para el usuario actual
    ajustes_usuario, created = Ajustes.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        form = AjustesForm(request.POST, instance=ajustes_usuario)
        if form.is_valid():
            ajustes = form.save(commit=False)
            ajustes.usuario = request.user
            ajustes.save()
            return redirect('ajustes:ajustes')
    else:
        form = AjustesForm(instance=ajustes_usuario)
    
    return render(request, 'ajustes/ajustes.html', {'form': form})
