from app.shared.db import db
from datetime import datetime

class ClusterInfo(db.Model):
    __tablename__ = "cluster_info"

    id = db.Column(db.Integer, primary_key=True)
    cluster_id = db.Column(db.Integer, nullable=False)
    cardinality = db.Column(db.Integer, nullable=False)
    most_frequent_title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    top_skills = db.Column(db.Text, nullable=True)
    top_sector = db.Column(db.String(255), nullable=True)