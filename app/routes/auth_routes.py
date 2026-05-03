from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

from app.models import User, AccountStatus
from app.utils.responses import ok, fail

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    identifier = (data.get("identifier") or "").strip()
    password = data.get("password") or ""

    if not identifier or not password:
        return fail("identifier and password are required.", code=400)

    user = User.query.filter(
        (User.username == identifier) |
        (User.email == identifier) |
        (User.phone == identifier)
    ).first()

    if not user or not user.check_password(password):
        return fail("Invalid credentials.", code=401)

    if user.status != AccountStatus.ACTIVE.value:
        return fail("Account is inactive. Contact admin.", code=403)

    claims = {"role": user.role, "status": user.status}

    access = create_access_token(identity=str(user.id), additional_claims=claims)
    refresh = create_refresh_token(identity=str(user.id), additional_claims=claims)

    return ok({
        "access_token": access,
        "refresh_token": refresh,
        "user": user.to_dict()
    }, "Login success")


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id_str = get_jwt_identity()

    try:
        user_id = int(user_id_str)
    except (TypeError, ValueError):
        return fail("Invalid token subject.", code=401)

    user = User.query.get(user_id)
    if not user:
        return fail("User not found.", code=404)
    if user.status != AccountStatus.ACTIVE.value:
        return fail("Account is inactive.", code=403)

    claims = {"role": user.role, "status": user.status}

    access = create_access_token(identity=str(user.id), additional_claims=claims)
    return ok({"access_token": access}, "Token refreshed")
