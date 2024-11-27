from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout,update_session_auth_hash
from .forms import RegistroForm,ApoderadoForm, AdministradorForm, AlumnoForm, ProfesorForm, EditarForm, EditarFotoPerfilForm, EditarCorreoForm, CambiarContraseñaForm, CambiarApoderado
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Perfil, Administrador,Alumno,Apoderado,Profesor
from django.shortcuts import get_object_or_404
from asignatura.models import Asignatura
from calificacion.models import Calificacion
from evaluacion.models import Evaluacion
from django.urls import reverse

@login_required
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
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
    if request.user.is_authenticated:
        perfil = Perfil.objects.get(user=request.user)
        if perfil.rol == 'administrador':
            return redirect('usuarios:menu_administrador')
        elif perfil.rol == 'profesor':
            return redirect('usuarios:menu_profesor')
        elif perfil.rol == 'apoderado':
            return redirect('usuarios:menu_apoderado')
        else:
            return redirect('usuarios:menu_alumno')
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
@login_required
def crear_administrador(request, user_id):
    perfil = Perfil.objects.get(id=user_id)

    if request.method == 'POST':
        form = AdministradorForm(request.POST)
        if form.is_valid():
            administrador = form.save(commit=False)
            administrador.perfil = perfil 
            administrador.save()
            messages.success(request, 'Administrador creado exitosamente.')
            return redirect('usuarios:lista_usuarios')  
    else:
        form = AdministradorForm()

    return render(request, 'usuarios/crear_administrador.html', {'form': form})
@login_required
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
@login_required
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
@login_required
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
@login_required
def lista_usuarios(request):
    rol_filtrado = request.GET.get('rol', None)  # Obtener el rol filtrado de la URL

    if rol_filtrado:
        usuarios = Perfil.objects.filter(rol=rol_filtrado, user__is_superuser=False)  # Filtrar por rol y excluir superusuarios
    else:
        usuarios = Perfil.objects.filter(user__is_superuser=False)  # Excluir superusuarios si no se filtra

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
    jefatura = getattr(usuario.perfil.profesor, 'jefatura', None)
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

    # Obtener todas las calificaciones del alumno
    calificaciones = Calificacion.objects.filter(alumno=alumno)

    # Obtener las evaluaciones asociadas al curso del alumno
    evaluaciones = Evaluacion.objects.filter(asignatura__curso=alumno.curso)

    # Calcular el promedio por asignatura
    promedios = {}

    # Agrupar las calificaciones por asignatura y calcular el promedio
    for calificacion in calificaciones:
        asignatura = calificacion.evaluacion.asignatura
        if asignatura not in promedios:
            promedios[asignatura] = {
                'total_calificaciones': 0,
                'cantidad': 0
            }
        promedios[asignatura]['total_calificaciones'] += calificacion.calificacion
        promedios[asignatura]['cantidad'] += 1
    
    # Calcular el promedio final para cada asignatura
    for asignatura, data in promedios.items():
        data['promedio'] = data['total_calificaciones'] / data['cantidad']

    # Pasar los datos al template
    return render(request, 'usuarios/detalle_alumno.html', {
        'alumno': alumno,
        'calificaciones': calificaciones,
        'evaluaciones': evaluaciones,
        'promedios': promedios,
    })
@login_required
def editar_perfil(request):
    user = request.user
    perfil = user.perfil

    # Formulario para editar foto de perfil
    foto_form = EditarFotoPerfilForm(instance=perfil)
    # Formulario para editar correo
    correo_form = EditarCorreoForm(instance=user)
    # Formulario para cambiar contraseña
    contraseña_form = CambiarContraseñaForm()

    if request.method == "POST":
        if "editar_foto" in request.POST:
            # Redirigir a editar foto
            return redirect('usuarios:editar_foto')
        elif "editar_correo" in request.POST:
            # Redirigir a editar correo
            return redirect('usuarios:editar_correo')
        elif "cambiar_contraseña" in request.POST:
            # Redirigir a cambiar contraseña
            return redirect('usuarios:cambiar_contraseña')

    context = {
        'foto_form': foto_form,
        'correo_form': correo_form,
        'contraseña_form': contraseña_form,
    }
    return render(request, 'usuarios/editar_perfil.html', context)
@login_required
def editar_foto(request):
    user = request.user
    perfil = user.perfil
    if request.method == "POST":
        foto_form = EditarFotoPerfilForm(request.POST, request.FILES, instance=perfil)
        if foto_form.is_valid():
            foto_form.save()
            messages.success(request, "Foto de perfil actualizada.")
            return redirect('usuarios:editar_perfil')
    else:
        foto_form = EditarFotoPerfilForm(instance=perfil)
    
    return render(request, 'usuarios/editar_foto.html', {'foto_form': foto_form})
@login_required
def editar_correo(request):
    user = request.user
    if request.method == "POST":
        correo_form = EditarCorreoForm(request.POST, instance=user)
        if correo_form.is_valid():
            correo_form.save()
            messages.success(request, "Correo electrónico actualizado.")
            return redirect('usuarios:editar_perfil')
    else:
        correo_form = EditarCorreoForm(instance=user)
    
    return render(request, 'usuarios/editar_correo.html', {'correo_form': correo_form})
@login_required
def cambiar_contraseña(request):
    user = request.user
    if request.method == "POST":
        contraseña_form = CambiarContraseñaForm(request.POST)
        if contraseña_form.is_valid():
            password_actual = contraseña_form.cleaned_data['password_actual']
            nueva_password = contraseña_form.cleaned_data['nueva_password']
            confirmar_password = contraseña_form.cleaned_data['confirmar_password']
            
            if nueva_password == confirmar_password:
                if user.check_password(password_actual):
                    user.set_password(nueva_password)
                    user.save()
                    update_session_auth_hash(request, user)  # Mantiene la sesión activa después de cambiar la contraseña
                    messages.success(request, "Contraseña actualizada con éxito.")
                    return redirect('usuarios:editar_perfil')
                else:
                    messages.error(request, "La contraseña actual no es correcta.")
            else:
                messages.error(request, "Las nuevas contraseñas no coinciden.")
    else:
        contraseña_form = CambiarContraseñaForm()

    return render(request, 'usuarios/cambiar_contraseña.html', {'contraseña_form': contraseña_form})
@login_required
def editar_administrador(request, user_id):
    administrador = get_object_or_404(Administrador, perfil_id=user_id)
    if request.method == 'POST':
        form = AdministradorForm(request.POST, instance=administrador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Administrador actualizado exitosamente.')
            return redirect(reverse('usuarios:detalle_usuario', args=[user_id]))
    else:
        form = AdministradorForm(instance=administrador)
    return render(request, 'usuarios/editar_administrador.html', {'form': form})

@login_required
def editar_profesor(request, user_id):
    profesor = get_object_or_404(Profesor, perfil_id=user_id)
    if request.method == 'POST':
        form = ProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profesor actualizado exitosamente.')
            return redirect(reverse('usuarios:detalle_usuario', args=[user_id]))
    else:
        form = ProfesorForm(instance=profesor)
    return render(request, 'usuarios/editar_profesor.html', {'form': form})

@login_required
def editar_apoderado(request, user_id):
    apoderado = get_object_or_404(Apoderado, perfil_id=user_id)
    if request.method == 'POST':
        form = ApoderadoForm(request.POST, instance=apoderado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Apoderado actualizado exitosamente.')
            return redirect(reverse('usuarios:detalle_usuario', args=[user_id]))
    else:
        form = ApoderadoForm(instance=apoderado)
    return render(request, 'usuarios/editar_apoderado.html', {'form': form})

@login_required
def editar_alumno(request, user_id):
    alumno = get_object_or_404(Alumno, perfil_id=user_id)
    
    if request.method == 'POST':
        form = CambiarApoderado(request.POST)
        if form.is_valid():
            alumno.apoderado = form.cleaned_data['apoderado']
            alumno.save()
            return redirect(reverse('usuarios:detalle_usuario', args=[user_id]))
    else:
        form = CambiarApoderado(initial={'apoderado': alumno.apoderado})

    return render(request, 'usuarios/editar_alumno.html', {'form': form})
@login_required
def borrar_usuario(request, user_id):
    perfil = get_object_or_404(Perfil, id=user_id)
    if request.method == 'POST':
        # Borra el usuario y su perfil asociado
        perfil.user.delete()
        perfil.delete()
        return redirect('usuarios:lista_usuarios')
    return render(request, 'usuarios/borrar_usuario_confirmacion.html', {'perfil': perfil})