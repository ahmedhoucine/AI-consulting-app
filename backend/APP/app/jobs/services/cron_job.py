from app.jobs.repositories.job_repository import JobRepository
from app.jobs.services.job_service import JobService

def cron_job(app):
   
    job_service = JobService(JobRepository())
    with app.app_context():
        job_service.load_data_from_api()
        job_service.reinitialize_cluster_recommendation()
