from shared.db import db 
from datetime import date 
class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recommandation_id = db.Column(db.Integer, nullable=False)
    note_consultant = db.Column(db.Integer)
    note_entreprise = db.Column(db.Integer)
    commentaire_consultant = db.Column(db.Text)
    commentaire_entreprise = db.Column(db.Text)
    date_feedback = db.Column(db.Date, default=date.today)

    def __repr__(self):
        return f"<Feedback {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "recommandation_id": self.recommandation_id,
            "note_consultant": self.note_consultant,
            "note_entreprise": self.note_entreprise,
            "commentaire_consultant": self.commentaire_consultant,
            "commentaire_entreprise": self.commentaire_entreprise,
            "date_feedback": self.date_feedback.isoformat() if self.date_feedback else None,
        }

