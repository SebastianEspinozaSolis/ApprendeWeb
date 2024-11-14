from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm,ApoderadoForm, AdministradorForm, AlumnoForm, ProfesorForm, EditarForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Perfil, Administrador,Alumno,Apoderado,Profesor
from django.shortcuts import get_object_or_404
from asignatura.models import Asignatura
from calificacion.models import Calificacion
from evaluacion.models import Evaluacion


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Asignamos datos al perfil
            user.perfil.rol = form.cleaned_data['rol']
            user.perfil.nombre = form.cleaned_data['nombre']
            user.perfil.rut = form.cleaned_data['rut']
            user.perfil.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
            user.perfil.sexo = form.cleaned_data['sexo']
            user.perfil.foto = form.cleaned_data['foto']
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

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            perfil = Perfil.objects.get(user=usuario)
            if perfil.rol == 'administrador':
                return redirect('usuarios:menu_administrador')
            elif perfil.rol == 'profesor':
                return redirect('usuarios:menu_profesor')
            elif perfil.rol == 'apoderado':
                return redirect('usuarios:menu_apoderado')
            else:
                return redirect('usuarios:menu_alumno')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'usuarios/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('usuarios:login')

def crear_administrador(request, user_id):
    perfil = Perfil.objects.get(id=user_id)

    if request.method == 'POST':
        form = AdministradorForm(request.POST)
        if form.is_valid():
            administrador = form.save(commit=False)
            administrador.perfil = perfil 
            administrador.save()
            messages.success(request, 'Administrador creado exitosamente.')
            return redirect('usuarios:login')  
    else:
        form = AdministradorForm()

    return render(request, 'usuarios/crear_administrador.html', {'form': form})

def crear_profesor(request, user_id):
    perfil = Perfil.objects.get(id=user_id) 

    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            profesor = form.save(commit=False)
            profesor.perfil = perfil 
            profesor.save()
            messages.success(request, 'Profesor creado exitosamente.')
            return redirect('usuarios:lista_usuarios')
    else:
        form = ProfesorForm()

    return render(request, 'usuarios/crear_profesor.html', {'form': form})

def crear_apoderado(request, user_id):
    perfil = Perfil.objects.get(id=user_id)

    if request.method == 'POST':
        form = ApoderadoForm(request.POST)
        if form.is_valid():
            apoderado = form.save(commit=False)
            apoderado.perfil = perfil  
            apoderado.save()
            messages.success(request, 'Apoderado creado exitosamente.')
            return redirect('usuarios:lista_usuarios')  
    else:
        form = ApoderadoForm()

    return render(request, 'usuarios/crear_apoderado.html', {'form': form})

def crear_alumno(request, user_id):
    perfil = Perfil.objects.get(id=user_id)

    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.perfil = perfil  
            alumno.save()
            messages.success(request, 'Alumno creado exitosamente.')
            return redirect('usuarios:lista_usuarios')  
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
@login_required
def editar_usuario(request, user_id):
    perfil = get_object_or_404(Perfil, id=user_id)
    if request.method == 'POST':
        form = EditarForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('usuarios:lista_usuarios') 
    else:
        form = EditarForm(instance=perfil)
    return render(request, 'usuarios/editar_usuario.html', {'form': form})
@login_required
def detalle_usuario(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    edad = perfil.calcular_edad()
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
        'edad': edad,
    })

@login_required
def menu_administrador(request):
    usuario = request.user
    return render(request, 'usuarios/menu_administrador.html', {
        'usuario': usuario, 
    })

@login_required
def menu_profesor(request):
    usuario = request.user
    asignaturas = Asignatura.objects.filter(profesor=usuario.perfil.profesor)
    jefatura = usuario.perfil.profesor.jefatura
    return render(request, 'usuarios/menu_profesor.html', {
        'usuario': usuario, 
        'asignaturas': asignaturas,
        'jefatura': jefatura,
    })

@login_required
def menu_apoderado(request):
    # Obtiene el apoderado relacionado con el usuario logueado
    usuario = request.user
    apoderado = usuario.perfil.apoderado  # Relación del apoderado con el perfil del usuario
    alumnos = apoderado.alumno_set.all()  # Obtiene todos los alumnos asociados al apoderado
    
    return render(request, 'usuarios/menu_apoderado.html', {
        'usuario': usuario,  # Información del usuario logueado
        'alumnos': alumnos,  # Alumnos a cargo del apoderado
    })

@login_required
def menu_alumno(request):
    usuario = request.user
    try:
        alumno = Alumno.objects.get(perfil=usuario.perfil)  # Obtener el alumno asociado al perfil del usuario
    except Alumno.DoesNotExist:
        alumno = None  # Si no existe el alumno para el usuario

    return render(request, 'usuarios/menu_alumno.html', {
        'usuario': usuario,
        'alumno': alumno,  # Pasamos el objeto alumno a la plantilla
    })

@login_required
def detalle_alumno(request, id):
    # Obtener el alumno correspondiente
    alumno = get_object_or_404(Alumno, id=id)

    # Obtener las calificaciones del alumno en las evaluaciones disponibles
    calificaciones = Calificacion.objects.filter(alumno=alumno)

    # Si quieres mostrar las evaluaciones, puedes filtrarlas también
    evaluaciones = Evaluacion.objects.filter(asignatura__curso=alumno.curso)

    return render(request, 'usuarios/detalle_alumno.html', {
        'alumno': alumno,
        'calificaciones': calificaciones,
        'evaluaciones': evaluaciones,
    })