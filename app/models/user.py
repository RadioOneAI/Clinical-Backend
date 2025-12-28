from datetime import datetime, date
from enum import Enum

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event
from sqlalchemy.orm.attributes import get_history
from sqlalchemy.orm import relationship

from app.extensions import db


class Role(str, Enum):
    ADMIN = "admin"
    RECEPTIONIST = "receptionist"
    DOCTOR = "doctor"
    RADIOGRAPHER = "radiographer"
    RADIOLOGIST = "radiologist"
    PATIENT = "patient"


class AccountStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


LICENSE_REQUIRED_ROLES = {Role.DOCTOR, Role.RADIOGRAPHER, Role.RADIOLOGIST}


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(30), nullable=False)

    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(30), unique=True, nullable=False)

    license_number = db.Column(db.String(80), unique=True, nullable=True)
    address = db.Column(db.String(255), nullable=True)

    gender = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)

    password_hash = db.Column(db.String(255), nullable=False)

    status = db.Column(db.String(20), nullable=False, default=AccountStatus.ACTIVE.value)

    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_by = relationship("User", remote_side=[id], lazy="joined")

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "license_number": self.license_number,
            "address": self.address,

            # ✅ NEW FIELDS
            "gender": self.gender,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "age": self.age,

            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


# -------------------------
# Prevent editing role/license
# -------------------------

@event.listens_for(User, "before_update")
def prevent_role_or_license_edit(mapper, connection, target: User):

    role_hist = get_history(target, "role")
    if role_hist.has_changes():
        raise ValueError("Role cannot be updated.")

    lic_hist = get_history(target, "license_number")
    if lic_hist.has_changes():
        old = lic_hist.deleted[0] if lic_hist.deleted else None
        new = lic_hist.added[0] if lic_hist.added else None
        if old is not None and new != old:
            raise ValueError("License/registration number cannot be updated.")