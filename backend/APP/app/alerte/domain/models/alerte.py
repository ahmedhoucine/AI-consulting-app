from shared.db import db

class AlerteConsultantInactif(db.Model):
    __tablename__ = 'alerte_consultant_inactif'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_consultant = db.Column(db.Integer, nullable=False)
    nom_prenom = db.Column(db.String(100), nullable=False)
    date_derniere_mission = db.Column(db.Date)
    nbr_jrs_inactifs=db.Column(db.Integer)
    alerte_declenchee = db.Column(db.String(5), default='non')  # oui / non
    date_declenchement_alerte = db.Column(db.Date)
    action_recommandee = db.Column(db.Text)
    statut=db.Column(db.String(20))



class EvaluationConsultant(db.Model):
    __tablename__ = 'evaluation_consultants'

    id = db.Column(db.Integer, primary_key=True)
    consultant_id = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Integer)
    commentaire = db.Column(db.Text)
    date_evaluation = db.Column(db.Date)

class ProfilConsultant(db.Model):
    __tablename__='consultant'
    id=db.Column(db.Integer,primary_key=True)
    nom=db.Column(db.String(100))
    email=db.Column(db.String(100))
    cv=db.Column(db.Text)
    statut=db.Column(db.Enum('disponible','mission'))
    date_creation=db.Column(db.Date)
