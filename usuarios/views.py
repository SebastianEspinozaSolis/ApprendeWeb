from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm,ApoderadoForm, AdministradorForm, AlumnoForm, ProfesorForm, EditarForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Perfil, Administrador,Alumno,Apoderado,Profesor
from django.shortcuts import get_object_or_404


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # No guardamos aún para asignar la contraseña
            user.set_password(form.cleaned_data['password'])  # Encriptamos la contraseña con el método set_password, clean_data para obtener los datos limpios del formulario
            user.save()#Guardamos el usuario
            # Asignamos el rol al perfil
            user.perfil.rol = form.cleaned_data['rol']
            user.perfil.nombre = form.cleaned_data['nombre']
            user.perfil.rut = form.cleaned_data['rut']
            user.perfil.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
            user.perfil.sexo = form.cleaned_data['sexo']
            user.perfil.save()

            if form.cleaned_data['rol'] == 'administrador':
                return redirect('usuarios:crear_administrador', user_id=user.perfil.id)
            elif form.cleaned_data['rol'] == 'apoderado':
                return redirect('usuarios:crear_apoderado', user_id=user.perfil.id)
            elif form.cleaned_data['rol'] == 'profesor':
                return redirect('usuarios:crear_profesor', user_id=user.perfil.id)
            elif form.cleaned_data['rol'] == 'alumno':
                return redirect('usuarios:crear_alumno', user_id=user.perfil.id)
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):#Vista para el inicio de sesión
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)#Autenticamos al usuario con las credenciales
        if usuario is not None:
            login(request, usuario)#Iniciamos sesión
            perfil = Perfil.objects.get(user=usuario)
            if perfil.rol == 'administrador':
                return redirect('curso:crear_curso')
            elif perfil.rol == 'profesor':
                return redirect('curso:lista_cursos')
            elif perfil.rol == 'apoderado':
                return redirect('curso:lista_cursos')
            else:
                return redirect('curso:lista_cursos')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'usuarios/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('usuarios:login')

def crear_administrador(request, user_id):
    perfil = Perfil.objects.get(id=user_id)  # Cambié la forma de obtener el perfil directamente

    if request.method == 'POST':
        form = AdministradorForm(request.POST)
        if form.is_valid():
            administrador = form.save(commit=False)
            administrador.perfil = perfil  # Asignamos el perfil al administrador
            administrador.save()
            messages.success(request, 'Administrador creado exitosamente.')
            return redirect('usuarios:login')  # Redirige a login o a otra página según prefieras
    else:
        form = AdministradorForm()

    return render(request, 'usuarios/crear_administrador.html', {'form': form})

def crear_profesor(request, user_id):
    perfil = Perfil.objects.get(id=user_id)  # Aquí también cambié la forma de obtener el perfil

    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            profesor = form.save(commit=False)
            profesor.perfil = perfil  # Asignamos el perfil al profesor
            profesor.save()
            messages.success(request, 'Profesor creado exitosamente.')
            return redirect('usuarios:login')
    else:
        form = ProfesorForm()

    return render(request, 'usuarios/crear_profesor.html', {'form': form})

def crear_apoderado(request, user_id):
    perfil = Perfil.objects.get(id=user_id)

    if request.method == 'POST':
        form = ApoderadoForm(request.POST)
        if form.is_valid():
            apoderado = form.save(commit=False)
            apoderado.perfil = perfil  # Asignamos el perfil al apoderado
            apoderado.save()
            messages.success(request, 'Apoderado creado exitosamente.')
            return redirect('usuarios:login')  # Redirige a login o a otra página según prefieras
    else:
        form = ApoderadoForm()

    return render(request, 'usuarios/crear_apoderado.html', {'form': form})

def crear_alumno(request, user_id):
    perfil = Perfil.objects.get(id=user_id)

    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.perfil = perfil  # Asignamos el perfil al alumno
            alumno.save()
            messages.success(request, 'Alumno creado exitosamente.')
            return redirect('usuarios:login')  # Redirige a login o a otra página según prefieras
    else:
        form = AlumnoForm()

    return render(request, 'usuarios/crear_alumno.html', {'form': form})
def lista_usuarios(request):
    rol_filtrado = request.GET.get('rol', None)  # Obtener el rol filtrado de la URL
    if rol_filtrado:
        usuarios = Perfil.objects.filter(rol=rol_filtrado)  # Filtrar usuarios por rol
    else:
        usuarios = Perfil.objects.all()  # Obtener todos los usuarios si no se filtra

    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

def editar_usuario(request, user_id):
    perfil = get_object_or_404(Perfil, id=user_id)
    if request.method == 'POST':
        form = EditarForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('usuarios:lista_usuarios')  # Redirige a la lista de usuarios
    else:
        form = EditarForm(instance=perfil)
    return render(request, 'usuarios/editar_usuario.html', {'form': form})

def detalle_usuario(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)

    # Intenta obtener las instancias de los roles
    administrador = Administrador.objects.filter(perfil=perfil).first()
    apoderado = Apoderado.objects.filter(perfil=perfil).first()
    alumno = Alumno.objects.filter(perfil=perfil).first()
    profesor = Profesor.objects.filter(perfil=perfil).first()

    return render(request, 'usuarios/detalle_usuario.html', {
        'perfil': perfil,
        'administrador': administrador,
        'alumno': alumno,
        'apoderado': apoderado,
        'profesor': profesor,
    })