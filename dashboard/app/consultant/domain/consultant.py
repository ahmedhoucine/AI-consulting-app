from app.shared.db import db
from datetime import datetime

class Consultant(db.Model):
    __tablename__ = 'consultants'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cv = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)