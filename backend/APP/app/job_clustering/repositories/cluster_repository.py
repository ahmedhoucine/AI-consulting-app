import pandas as pd
from collections import Counter
from app.job_clustering.domain.cluster_entity import ClusterInfo
from app.shared.db import db

class ClusterRepository:
    def delete_all(self):
        db.session.query(ClusterInfo).delete()
        db.session.commit()
    def save_clusters(self, labels, original_data):
        self.delete_all()

        df = pd.DataFrame(original_data)
        df['cluster'] = labels

        for cluster_id in sorted(set(labels)):
            cluster_data = df[df['cluster'] == cluster_id]
            cardinality = len(cluster_data)

            # --- Most frequent Job Title ---
            most_frequent_title = cluster_data['Job Title'].mode()[0]

            # --- Top sector with fallback if most frequent is 'non spécifié' ---
            top_sector = None
            if 'Sector' in cluster_data.columns:
                sector_counts = (
                    cluster_data['Sector']
                    .dropna()
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .value_counts()
                )
                if not sector_counts.empty:
                    top_sector = sector_counts.index[0]
                    if top_sector == 'non spécifié' and len(sector_counts) > 1:
                        top_sector = sector_counts.index[1]


            # --- Top skills with fallback if most frequent is 'non spécifié' ---
            top_skills = None
            if 'Skills' in cluster_data.columns:
                all_skills = (
                    cluster_data['Skills']
                    .dropna()
                    .astype(str)
                    .str.lower()
                    .str.split(',')
                    .explode()
                    .str.strip()
                )
                skill_counts = all_skills.value_counts()

                if not skill_counts.empty:
                    # Default top skill
                    top_skill_candidate = skill_counts.index[0]

                    # If it's 'non spécifié', try the next best
                    if top_skill_candidate == 'non spécifié' and len(skill_counts) > 1:
                        top_skill_candidate = skill_counts.index[1]

                    top_skills = top_skill_candidate


            print(f"Cluster {cluster_id} | Title: {most_frequent_title} | Sector: {top_sector} | Skills: {top_skills}")

            record = ClusterInfo(
                cluster_id=cluster_id,
                cardinality=cardinality,
                most_frequent_title=most_frequent_title,
                top_sector=top_sector,
                top_skills=top_skills
            )
            db.session.add(record)

        db.session.commit()



    def get_all_clusters(self):
        return ClusterInfo.query.order_by(ClusterInfo.cluster_id).all()
