import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import torch

from app.jobs.services.job_service import JobService
from flask import current_app

class RecommendationEngine:
    def __init__(self):
        self.model = None
        self.hnsw_index = None
        self.data = None
        self.initialized = False

    def initialize(self):
        

        print("🚀 Initializing RecommendationEngine...")
        # Must be called within Flask app context
        with current_app.app_context():
            jobs = JobService.get_all_jobs()
            jobs_dicts = [job.__dict__ for job in jobs]

            self.data = pd.DataFrame(jobs_dicts)
            #self.data.rename(columns={'title': 'Job Title', 'description': 'Description', 'id': 'Job ID'}, inplace=True)
            self.data['job_with_description'] = self.data['job_title'] + '  ' + self.data['description']

            sentences = self.data['job_with_description'].dropna()
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
            print("Running encoding on:", self.model._target_device)

            sentence_vectors = self.model.encode(sentences, show_progress_bar=True).astype('float32')
            sentence_vectors = sentence_vectors / np.linalg.norm(sentence_vectors, axis=1, keepdims=True)

            d = sentence_vectors.shape[1]
            self.hnsw_index = faiss.IndexHNSWFlat(d, 32)
            self.hnsw_index.hnsw.efSearch = 64
            self.hnsw_index.hnsw.efConstruction = 200
            self.hnsw_index.add(sentence_vectors)

            self.initialized = True
                

    def get_recommendations(self, query: str, k=10):
        if not self.initialized:
            raise RuntimeError("RecommendationEngine is not initialized. Call initialize() first within app context.")

        query_vec = self.model.encode([query]).astype('float32')
        query_vec = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)
        _, ids = self.hnsw_index.search(query_vec, k)
        return self.data.iloc[ids[0]]['id'].tolist()
