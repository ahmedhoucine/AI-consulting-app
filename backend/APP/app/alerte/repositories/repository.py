from alerte.domain.models.alerte import AlerteConsultantInactif,EvaluationConsultant,ProfilConsultant
from shared.db import db 
from datetime import date
from sqlalchemy.orm import joinedload

def get_alertes():
    return AlerteConsultantInactif.query.all()


def update_alerte(alerte):
    db.session.commit()

def supprimer_alerte(alerte_id):
    alerte = AlerteConsultantInactif.query.get(alerte_id)
    if alerte:
        db.session.delete(alerte)
        db.session.commit()
        return True
    return False

def get_evaluations_by_consultant_id(consultant_id):
    return EvaluationConsultant.query.filter_by(consultant_id=consultant_id).all()

def get_profil_by_consultant_id(consultant_id):
    return ProfilConsultant.query.get(consultant_id)

def get_statut_consultant(consultant_id):
    profil = ProfilConsultant.query.get(consultant_id)
    return profil.statut if profil else None