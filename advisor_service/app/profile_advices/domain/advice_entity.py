from app.shared.db import db
from datetime import datetime

class AdviceRecord(db.Model):
    __tablename__ = 'advice_records'

    id = db.Column(db.Integer, primary_key=True)
    profile_description = db.Column(db.Text, nullable=False)
    target_job_title = db.Column(db.String(255), nullable=False)
    advice = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
