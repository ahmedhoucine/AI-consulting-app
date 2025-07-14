from flask import Blueprint, jsonify

from app.jobs.repositories.job_repository import JobRepository
from app.jobs.services.job_service import JobService

job_bp = Blueprint('routes', __name__)

@job_bp.route('/load-csv', methods=['POST'])
def load_csv():
    try:
        JobService.load_csv_from_path("data.csv")
        return jsonify({"message": "✅ CSV loaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@job_bp.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = JobService.get_job_by_id(job_id)
    if job is None:
        return jsonify({"error": "Job not found"}), 404

    # Convert job record to dict (you may want to customize this)
    job_data = {
        "id": job.id,
        "job_title": job.job_title,
        "publishing_date": job.publishing_date,
        "start_date": job.start_date,
        "salary": job.salary,
        "duration": job.duration,
        "location": job.location,
        "work_mode": job.work_mode,
        "skills": job.skills,
        "description": job.description,
        "plateforme": job.plateforme,
        "scrap_date": job.scrap_date,
        "company_name": job.company_name,
        "number_of_candidates": job.number_of_candidates,
        "number_of_employees": job.number_of_employees,
        "sector": job.sector,
        "description_e": job.description_e,
        "experience": job.experience,
        "contract_type": job.contract_type,
        "education": job.education,
        "scrap_date_parsed": job.scrap_date_parsed,
        "estm_publishdate": job.estm_publishdate,
    }

    return jsonify(job_data), 200

@job_bp.route('/api/jobs', methods=['GET'])
def get_all_jobs():
    jobs = JobService.get_all_jobs()

    job_list = []
    for job in jobs:
        job_list.append({
            "id": job.id,
            "job_title": job.job_title,
            "publishing_date": job.publishing_date,
            "start_date": job.start_date,
            "salary": job.salary,
            "duration": job.duration,
            "location": job.location,
            "work_mode": job.work_mode,
            "skills": job.skills,
            "description": job.description,
            "plateforme": job.plateforme,
            "scrap_date": job.scrap_date,
            "company_name": job.company_name,
            "number_of_candidates": job.number_of_candidates,
            "number_of_employees": job.number_of_employees,
            "sector": job.sector,
            "description_e": job.description_e,
            "experience": job.experience,
            "contract_type": job.contract_type,
            "education": job.education,
            "scrap_date_parsed": job.scrap_date_parsed,
            "estm_publishdate": job.estm_publishdate,
        })

    return jsonify(job_list), 200
