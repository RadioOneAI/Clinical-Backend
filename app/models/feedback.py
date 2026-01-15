from datetime import datetime
from app.extensions import db


class ReportFeedback(db.Model):
    __tablename__ = "report_feedbacks"

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("reports.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    report = db.relationship("Report", backref=db.backref("feedbacks", lazy=True, cascade="all, delete-orphan"))
    user = db.relationship("User", backref=db.backref("report_feedbacks", lazy=True))