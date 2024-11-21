from django.shortcuts import redirect
from functools import wraps

def profesor_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'perfil') and request.user.perfil.rol in ['profesor', 'administrador']:
            return view_func(request, *args, **kwargs)
        return redirect('home')  # o la URL que prefieras para usuarios no autorizados
    return wrapper 