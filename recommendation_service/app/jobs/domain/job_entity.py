from app.shared.db import db

class JobRecord(db.Model):
    __tablename__ = 'job_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_title = db.Column(db.String(255))
    publishing_date = db.Column(db.String(255))
    start_date = db.Column(db.String(255))
    salary = db.Column(db.String(255))
    duration = db.Column(db.String(255))
    location = db.Column(db.String(255))
    work_mode = db.Column(db.String(255))
    skills = db.Column(db.Text)
    description = db.Column(db.Text)
    plateforme = db.Column(db.String(255))
    scrap_date = db.Column(db.String(255))
    company_name = db.Column(db.String(255))
    number_of_candidates = db.Column(db.String(255))
    number_of_employees = db.Column(db.String(255))
    sector = db.Column(db.String(255))
    description_e = db.Column(db.Text)
    experience = db.Column(db.String(255))
    contract_type = db.Column(db.String(255))
    education = db.Column(db.String(255))
    scrap_date_parsed = db.Column(db.String(255))
    estm_publishdate = db.Column(db.String(255))
