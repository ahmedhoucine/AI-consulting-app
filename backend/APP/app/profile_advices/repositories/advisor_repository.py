from langchain_ollama.llms import OllamaLLM
from app.profile_advices.services.model import prompt
from app.profile_advices.domain.advice_entity import AdviceRecord
from app.shared.db import db
import os
from typing import Iterator, Union
from httpx import ConnectError

class AdvisorRepository:
    def __init__(self):
        # Configure with environment variable fallback
        ollama_host = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
        
        # Initialize LangChain Ollama client
        self.llm = OllamaLLM(
            model="mistral",
            base_url=ollama_host,
            temperature=0.7,  # Recommended to add temperature
            streaming=True
        )
        self.chain = prompt | self.llm

    def get_recommendations(self, profile_description: str, target_job_title: str, stream: bool = False) -> Union[str, Iterator[str]]:
        """Get recommendations from Ollama"""
        inputs = {
            "profile_description": profile_description,
            "target_job_title": target_job_title
        }

        try:
            if stream:
                return self.chain.stream(inputs)
            return self.chain.invoke(inputs)
        except ConnectError as e:
            raise ConnectionError(f"Failed to connect to Ollama at {self.llm.base_url}. Is it running?") from e

    def save_advice(self, profile_description: str, target_job_title: str, advice: str) -> None:
        """Save advice to database"""
        try:
            record = AdviceRecord(
                profile_description=profile_description,
                target_job_title=target_job_title,
                advice=advice
            )
            db.session.add(record)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Failed to save advice: {str(e)}") from e

    def get_all_advice(self):
        """Retrieve all advice records"""
        return AdviceRecord.query.order_by(AdviceRecord.created_at.desc()).all()