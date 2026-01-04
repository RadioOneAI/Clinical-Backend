from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request
from flask_jwt_extended import current_user

from app.extensions import db
from app.utils.responses import ok, fail
from app.utils.decorators import active_required
from datetime import datetime

profile_bp = Blueprint("profile", __name__, url_prefix="/api")


@profile_bp.get("/me")
@active_required
def get_me():
    return ok(current_user.to_dict(), "My profile")


@profile_bp.patch("/me")
@active_required
def update_me():
    data = request.get_json() or {}

    #not allowed to change these by anyone
    if "role" in data:
        return fail("role cannot be updated.", code=400)
    if "status" in data:
        return fail("status cannot be updated by staff.", code=400)
    if "license_number" in data:
        return fail("license_number cannot be updated.", code=400)

    #allowed fields (NOTE: remove password here if you want ONLY change-password endpoint)
    allowed = ["name", "username", "email", "phone", "address", "gender", "date_of_birth"]
    for key in list(data.keys()):
        if key not in allowed:
            data.pop(key, None)

    if "name" in data and data["name"]:
        current_user.name = data["name"].strip()

    if "username" in data and data["username"]:
        current_user.username = data["username"].strip()

    if "email" in data and data["email"]:
        current_user.email = data["email"].strip()

    if "phone" in data and data["phone"]:
        current_user.phone = data["phone"].strip()

    if "address" in data:
        current_user.address = (data.get("address") or "").strip()

    if "gender" in data:
        current_user.gender = (data.get("gender") or "").strip().lower() or None

    if "date_of_birth" in data:
        dob_str = (data.get("date_of_birth") or "").strip()

        if dob_str == "":
            current_user.date_of_birth = None
        else:
            try:
                current_user.date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                return fail("date_of_birth must be YYYY-MM-DD", code=400)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return fail("username/email/phone already exists.", code=409)
    except ValueError as e:
        db.session.rollback()
        return fail(str(e), code=400)

    return ok(current_user.to_dict(), "Profile updated")

@profile_bp.post("/me/change-password")
@active_required
def change_password():
    data = request.get_json() or {}

    old_password = data.get("old_password") or ""
    new_password = data.get("new_password") or ""
    confirm_password = data.get("confirm_password") or ""

    if not old_password or not new_password or not confirm_password:
        return fail("old_password, new_password, confirm_password are required.", code=400)

    if not current_user.check_password(old_password):
        return fail("Old password is incorrect.", code=401)

    if new_password != confirm_password:
        return fail("New password and confirm password do not match.", code=400)

    if len(new_password) < 8:
        return fail("New password must be at least 8 characters.", code=400)

    if old_password == new_password:
        return fail("New password must be different from old password.", code=400)

    current_user.set_password(new_password)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return fail("Failed to update password.", code=500)

    return ok(None, "Password changed successfully. Please login again.")
