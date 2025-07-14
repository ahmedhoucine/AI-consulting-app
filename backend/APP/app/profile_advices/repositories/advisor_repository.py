from langchain_ollama import OllamaLLM
from app.profile_advices.services.model import prompt
from app.profile_advices.domain.advice_entity import AdviceRecord
from app.shared.db import db

class AdvisorRepository:
    def __init__(self):
        self.llm = OllamaLLM(model="mistral", streaming=True)
        self.chain = prompt | self.llm

    def get_recommendations(self, profile_description: str, target_job_title: str, stream: bool = False):
        if stream:
            # Use .stream() for streaming token-by-token
            return self.chain.stream({
                "profile_description": profile_description,
                "target_job_title": target_job_title
            })
        else:
            # Use .invoke() for full response at once
            print("invoke")
            return self.chain.invoke({
                "profile_description": profile_description,
                "target_job_title": target_job_title
            })

    def save_advice(self, profile_description: str, target_job_title: str, advice: str) -> None:
        record = AdviceRecord(
            profile_description=profile_description,
            target_job_title=target_job_title,
            advice=advice
        )
        db.session.add(record)
        db.session.commit()

    def get_all_advice(self):
        return AdviceRecord.query.order_by(AdviceRecord.created_at.desc()).all()
