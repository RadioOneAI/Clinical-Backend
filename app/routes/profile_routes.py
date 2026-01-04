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
