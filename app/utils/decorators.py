from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, current_user

from app.utils.responses import fail
from app.models import Role, AccountStatus

def active_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if not current_user:
            return fail("Unauthorized", code=401)
        if current_user.status != AccountStatus.ACTIVE.value:
            return fail("Account is inactive. Contact admin.", code=403)
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if not current_user:
            return fail("Unauthorized", code=401)
        if current_user.status != AccountStatus.ACTIVE.value:
            return fail("Account is inactive.", code=403)
        if current_user.role != Role.ADMIN.value:
            return fail("Admin access required.", code=403)
        return fn(*args, **kwargs)
    return wrapper



