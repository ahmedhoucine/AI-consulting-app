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


class SemanticEmbedder(BaseEstimator, TransformerMixin):
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = SentenceTransformer(model_name, device=self.device)
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return self.model.encode(X, convert_to_numpy=True, batch_size=32, show_progress_bar=True)

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

def prepare_and_cluster_data(filepath="data.csv"):
    data = pd.read_csv(filepath)
    data = data.drop(columns=["ID", "Scrap Date", "scrap_date_parsed", "Duration", "Location"], errors='ignore')

    num_attribs = ['Number of Candidates', 'Number of Employees']
    cat_attribs = ['Job Title', 'Work Mode', 'Plateforme', 'Company Name', 'Sector', "Salary", 'Contract Type', 'Education']
    text_attrib = ['Description']

    num_pipeline = Pipeline([
        ('selector', DataFrameSelector(num_attribs)),
        ('cleaner', NumericCleaner()),
        ('imputer', SimpleImputer(strategy="median")),
        ('scaler', StandardScaler()),
    ])

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

    full_pipeline = Pipeline([
        ('features', FeatureUnion([
            ('num', num_pipeline),
            ('cat', cat_pipeline),
            ('text', text_pipeline)
        ])),
        ('final_imputer', SimpleImputer(strategy='constant', fill_value=0))
    ])

    # Apply transformation
    X = full_pipeline.fit_transform(data)

    # Dimensionality reduction before clustering
    svd = TruncatedSVD(n_components=14, random_state=42)
    reduced = svd.fit_transform(X)
    scaled = StandardScaler().fit_transform(reduced)

    # HDBSCAN clustering
    clusterer = hdbscan.HDBSCAN(min_cluster_size=30, metric='euclidean')
    labels = clusterer.fit_predict(scaled)

    # Number of clusters (excluding noise)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print(f"✅ Number of clusters found by HDBSCAN: {n_clusters}")

    # Optional silhouette score
    if n_clusters > 1 and len(set(labels)) < len(scaled):
        score = silhouette_score(scaled, labels)
        print(f"📊 Silhouette Score: {score:.4f}")

    return labels, data
