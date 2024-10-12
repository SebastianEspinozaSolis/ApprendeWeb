from django.shortcuts import render

# Create your views here.
def iniciosesion(request):
 return render(request, 'InicioSesion/iniciosesion.html')