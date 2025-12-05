from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def role_required(roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            employee = getattr(request.user, 'employee', None)

            if employee is None or employee.role not in roles:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
