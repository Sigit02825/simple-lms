from functools import wraps
from ninja.errors import HttpError

def is_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.auth:
                raise HttpError(401, "Unauthorized")
            if request.auth.role != role and request.auth.role != 'admin':
                raise HttpError(403, f"Forbidden: Requires {role} role")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

is_instructor = is_role('instructor')
is_student = is_role('student')
is_admin = is_role('admin')
