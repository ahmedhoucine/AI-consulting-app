from app.shared.db import db
from datetime import datetime

class DashboardSnapshot(db.Model):
    __tablename__ = 'dashboard_snapshots'

    id = db.Column(db.Integer, primary_key=True)

    offre_count = db.Column(db.Integer, nullable=False, default=0)
    success_rate = db.Column(db.Float, nullable=False, default=0.0)

    consultant_status = db.Column(db.JSON, nullable=False)  # {disponible, en_mission, inactif}
    top_jobs = db.Column(db.JSON, nullable=False)  # [{nom, total_occurences}]
    top_skills = db.Column(db.JSON, nullable=False)  # [{skill, occurrences}]
    top_secteurs = db.Column(db.JSON, nullable=False)  # [{nom, total_occurences}]
    top_entreprises = db.Column(db.JSON, nullable=False)  # [{company_name, total}]
    bottom_entreprises = db.Column(db.JSON, nullable=False)  # [] or [{company_name, total}]
    offres_par_localisation = db.Column(db.JSON, nullable=False)  # [{location, total}]

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
