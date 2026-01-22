from datetime import datetime
from enum import Enum

from app.extensions import db


class PrescriptionStatus(str, Enum):
    PENDING = "pending"
    SCANNED = "scanned"
    REPORTED = "reported"


class Prescription(db.Model):
    __tablename__ = "prescriptions"

    id = db.Column(db.Integer, primary_key=True)
    scan_req_id = db.Column(db.String(50), unique=True, nullable=False)

    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    radiologist_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    scan_type = db.Column(db.String(80), nullable=False)
    organ = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)

    status = db.Column(
        db.String(30),
        nullable=False,
        default=PrescriptionStatus.PENDING.value,
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # one-to-one: one prescription can have one report
    report = db.relationship(
        "Report",
        back_populates="prescription",
        uselist=False,
        lazy=True,
    )

    prescription_images = db.relationship(
        "PrescriptionImage",
        backref="prescription",
        cascade="all, delete-orphan",
        lazy=True,
    )


class PrescriptionImage(db.Model):
    __tablename__ = "prescription_images"

    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey("prescriptions.id"), nullable=False)

    file_path = db.Column(db.String(255), nullable=False)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)