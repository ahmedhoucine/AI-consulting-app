from app.profile_advices.repositories.advisor_repository import AdvisorRepository

class AdvisorService:
    def __init__(self):
        self.repo = AdvisorRepository()

    def generate_advice(self, profile_description: str, target_job_title: str) -> str:
        advice = self.repo.get_recommendations(profile_description, target_job_title)
        self.repo.save_advice(profile_description, target_job_title, advice)
        return advice
    def get_history(self):
        return self.repo.get_all_advice()
