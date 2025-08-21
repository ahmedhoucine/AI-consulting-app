from flask import Blueprint, jsonify, request
from app.jobs.repositories.job_repository import JobRepository
from app.jobs.services.job_service import JobService

job_bp = Blueprint('jobs', __name__)
job_service = JobService(JobRepository())

def serialize_job(job):
    """Convert Job model to dictionary."""
    return {
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

@job_bp.route('/load-csv', methods=['POST'])
def load_csv():
    job_service.load_data_from_api()
    job_service.reinitialize_cluster_recommendation()
    return jsonify({"message": "data scraped and  loaded successfully"}), 200


@job_bp.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id: int):
    """Get a single job by ID."""
    job = job_service.get_job_by_id(job_id)
    if job is None:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(serialize_job(job)), 200

@job_bp.route('/api/jobs', methods=['GET'])
def get_all_jobs():
    """Get a list of all jobs."""
    jobs = job_service.get_all_jobs()
    return jsonify([serialize_job(job) for job in jobs]), 200
