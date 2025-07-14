from app.shared.db import db
from datetime import datetime

class RecommendationRecord(db.Model):
    __tablename__ = 'recommendation_records'

    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.Text, nullable=False)
    recommendations = db.Column(db.Text, nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
