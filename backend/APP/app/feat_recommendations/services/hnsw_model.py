import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import torch
from flask import current_app

from app.jobs.services.job_service import JobService


class RecommendationEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2', hnsw_m=32, ef_search=64, ef_construction=200):
        self.model_name = model_name
        self.hnsw_m = hnsw_m
        self.ef_search = ef_search
        self.ef_construction = ef_construction
        
        self.model = None
        self.hnsw_index = None
        self.data = None
        self.initialized = False

    def initialize(self):
        """Initialize the recommendation engine: load jobs, encode them, and build the FAISS index."""
        with current_app.app_context():
            jobs_df = self._load_jobs()
            if jobs_df.empty:
                raise ValueError("No jobs found to build recommendation index.")

            self.data = jobs_df
            embeddings = self._encode_sentences(jobs_df['job_with_description'].dropna())
            self._build_faiss_index(embeddings)

            self.initialized = True
            print("✅ RecommendationEngine initialized with", len(self.data), "jobs.")

    def _load_jobs(self) -> pd.DataFrame:
        """Fetch jobs from JobService and prepare DataFrame."""
        jobs = JobService.get_all_jobs()
        df = pd.DataFrame([job.__dict__ for job in jobs])
        if 'job_title' not in df or 'description' not in df:
            raise KeyError("Missing required job fields in data.")
        df['job_with_description'] = df['job_title'] + '  ' + df['description']
        return df

    def _encode_sentences(self, sentences):
        """Encode job descriptions into vector embeddings."""
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = SentenceTransformer(self.model_name, device=device)
        print(f"🚀 Encoding on device: {device}")
        
        vectors = self.model.encode(sentences, show_progress_bar=True).astype('float32')
        return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)  # Normalize for cosine sim

    def _build_faiss_index(self, embeddings):
        """Build FAISS HNSW index from embeddings."""
        d = embeddings.shape[1]
        self.hnsw_index = faiss.IndexHNSWFlat(d, self.hnsw_m)
        self.hnsw_index.hnsw.efSearch = self.ef_search
        self.hnsw_index.hnsw.efConstruction = self.ef_construction
        self.hnsw_index.add(embeddings)

    def get_recommendations(self, query: str, k=10):
        """Return top-k job IDs similar to the query string."""
        if not self.initialized:
            raise RuntimeError("Engine not initialized. Call initialize() first.")
        
        query_vec = self.model.encode([query]).astype('float32')
        query_vec = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)
        
        _, ids = self.hnsw_index.search(query_vec, k)
        return self.data.iloc[ids[0]]['id'].tolist()
