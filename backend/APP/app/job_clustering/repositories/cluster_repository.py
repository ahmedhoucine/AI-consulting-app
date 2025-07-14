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
            most_frequent_title = cluster_data['Job Title'].mode()[0]  
            count = cluster_data['Job Title'].value_counts()[most_frequent_title]
            print(f"Most frequent job title: {most_frequent_title}, Count: {count}")
            record = ClusterInfo(
                cluster_id=cluster_id,
                cardinality=cardinality,
                most_frequent_title=most_frequent_title
            )
            db.session.add(record)

        db.session.commit()

    def get_all_clusters(self):
        return ClusterInfo.query.order_by(ClusterInfo.cluster_id).all()
