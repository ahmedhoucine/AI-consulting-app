from app.job_clustering.services.clustering_pipeline import prepare_and_cluster_data
from app.job_clustering.repositories.cluster_repository import ClusterRepository

class ClusterService:
    def __init__(self):
        self.repo = ClusterRepository()

    def run_and_save_clusters(self):
        
        labels, data = prepare_and_cluster_data()
        self.repo.save_clusters(labels, data[["Job Title"]]) 

    def get_clusters(self):
        return self.repo.get_all_clusters()
