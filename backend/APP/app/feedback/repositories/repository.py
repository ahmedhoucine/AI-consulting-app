from feedback.domain.models.feedback import Feedback
from shared.db import db

def get_all_feedbacks():
    return Feedback.query.all()


