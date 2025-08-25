import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import TruncatedSVD
from sentence_transformers import SentenceTransformer
import numpy as np
import torch
import hdbscan
from sklearn.metrics import silhouette_score
from sqlalchemy import create_engine

from app.config import Config

NON_SPECIFIED = "non spécifié"

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)


# ---------- Transformers ----------
class SemanticEmbedder(BaseEstimator, TransformerMixin):
    def __init__(self, model_name='all-MiniLM-L6-v2', batch_size=32):
        self.model_name = model_name
        self.batch_size = batch_size
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = SentenceTransformer(model_name, device=self.device)
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return self.model.encode(X, convert_to_numpy=True, batch_size=self.batch_size, show_progress_bar=True)

class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names, as_text=False):
        self.attribute_names = attribute_names
        self.as_text = as_text
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        if self.as_text:
            return X[self.attribute_names[0]].astype(str).values
        return X[self.attribute_names].values

class NumericCleaner(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return np.column_stack([
            pd.to_numeric(pd.Series(X[:, i]), errors='coerce').values
            for i in range(X.shape[1])
        ])

# ---------- Pipeline Builders ----------
def build_feature_pipeline( cat_attribs, text_attrib):
   

    cat_pipeline = Pipeline([
        ('selector', DataFrameSelector(cat_attribs)),
        ('imputer', SimpleImputer(strategy="most_frequent")),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=True)),
    ])

    text_pipeline = Pipeline([
        ('selector', DataFrameSelector(text_attrib, as_text=True)),
        ('embedder', SemanticEmbedder()),
        ('svd', TruncatedSVD(n_components=50, random_state=42)),
    ])

    """ num_pipeline = Pipeline([
        ('selector', DataFrameSelector(num_attribs)),
        ('cleaner', NumericCleaner()),
        ('imputer', SimpleImputer(strategy="median")),
        ('scaler', StandardScaler()),
    ])"""

    return FeatureUnion([
       # ('num', num_pipeline),
        ('cat', cat_pipeline),
        ('text', text_pipeline)
    ])

# ---------- Main Logic ----------
def prepare_and_cluster_data(min_cluster_size=30, n_components=14):
    """Read data from DB, preprocess, cluster, and return labels + processed DataFrame."""
    data = load_and_clean_data(engine)
    pipeline = build_feature_pipeline(
        #num_attribs=['number_of_candidates', 'number_of_employees'],
        cat_attribs=['job_title', 'work_mode', 'plateforme', 'company_name', 'sector', "salary", 'contract_type', 'education'],
        text_attrib=['description']
    )

    X = pipeline.fit_transform(data)

    reduced = TruncatedSVD(n_components=n_components, random_state=42).fit_transform(X)
    scaled = StandardScaler().fit_transform(reduced)

    labels = cluster_data(scaled, min_cluster_size)

    return labels, data


def load_and_clean_data(engine):
    """Load dataset from job_records table and drop unnecessary columns."""
    query = "SELECT * FROM job_records"
    df = pd.read_sql(query, engine)
    return df.drop(
        columns=["ID", "Scrap Date", "scrap_date_parsed", "Duration", "Location"],
        errors='ignore'
    )

def cluster_data(X, min_cluster_size):
    """Run HDBSCAN clustering and optionally print metrics."""
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric='euclidean')
    labels = clusterer.fit_predict(X)

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print(f"✅ Number of clusters: {n_clusters}")

    if n_clusters > 1:
        score = silhouette_score(X, labels)
        print(f"📊 Silhouette Score: {score:.4f}")

    return labels
