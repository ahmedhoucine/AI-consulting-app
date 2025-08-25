import pandas as pd
from app.job_clustering.domain.cluster_entity import ClusterInfo
from app.shared.db import db

NON_SPECIFIED = "non spécifié"

class ClusterRepository:

    def delete_all(self):
        """Remove all cluster records from the database."""
        db.session.query(ClusterInfo).delete()
        db.session.commit()

    def save_clusters(self, labels, original_data):
        """Save clusters with their metadata (cardinality, top title, sector, skills)."""
        self.delete_all()

        df = pd.DataFrame(original_data)
        df['cluster'] = labels

        for cluster_id in sorted(set(labels)):
            record = self._create_cluster_record(df, cluster_id)
            db.session.add(record)

        db.session.commit()

    def _create_cluster_record(self, df, cluster_id):
        """Generate a ClusterInfo object for a given cluster_id."""
        cluster_data = df[df['cluster'] == cluster_id]
        
        return ClusterInfo(
            cluster_id=cluster_id,
            cardinality=len(cluster_data),
            most_frequent_title=self._get_most_frequent(cluster_data, 'job_title'),
            top_sector=self._get_most_frequent(cluster_data, 'sector'),
            top_skills=self._get_top_skill(cluster_data)
        )

    def _get_most_frequent(self, df, column):
        """Return the most frequent value in a column, skipping NON_SPECIFIED if possible."""
        if column not in df.columns:
            return None

        counts = (
            df[column]
            .dropna()
            .astype(str)
            .str.strip()
            .str.lower()
            .value_counts()
        )

        return self._get_best_candidate(counts)

    def _get_top_skill(self, df):
        """Return the most frequent skill in the Skills column."""
        if 'Skills' not in df.columns:
            return None

        all_skills = (
            df['Skills']
            .dropna()
            .astype(str)
            .str.lower()
            .str.split(',')
            .explode()
            .str.strip()
        )

        counts = all_skills.value_counts()
        return self._get_best_candidate(counts)

    def _get_best_candidate(self, counts):
        """Helper: pick the most frequent value, skipping NON_SPECIFIED if possible."""
        if counts.empty:
            return None

        top_candidate = counts.index[0]
        if top_candidate == NON_SPECIFIED and len(counts) > 1:
            return counts.index[1]
        return top_candidate

    def get_all_clusters(self):
        """Fetch all clusters ordered by ID."""
        return ClusterInfo.query.order_by(ClusterInfo.cluster_id).all()
