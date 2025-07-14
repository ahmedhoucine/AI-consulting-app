import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sentence_transformers import SentenceTransformer
import numpy as np
import torch


class SemanticEmbedder(BaseEstimator, TransformerMixin):
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = SentenceTransformer(model_name, device=self.device)
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return self.model.encode(X, convert_to_numpy=True, batch_size=32, show_progress_bar=False)

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

    X = full_pipeline.fit_transform(data)

    # Dimensionality reduction before clustering
    svd = TruncatedSVD(n_components=14, random_state=42)
    reduced = svd.fit_transform(X)
    scaled = StandardScaler().fit_transform(reduced)

    # Progressive step-wise search for best k
    def find_best_k_progressively(X, initial_step=5, min_step=1, max_no_improve_rounds=2):
        best_k = 2
        best_score = -1
        step = initial_step
        last_best_k = -1
        no_improve_rounds = 0

        current_range = list(range(2, 50, step))

        while step >= min_step and no_improve_rounds < max_no_improve_rounds:
            print(f"\n🔎 Testing k in range: {current_range}")
            improvement = False

            for k in current_range:
                km = KMeans(n_clusters=k, random_state=42, n_init="auto")
                labels = km.fit_predict(X)
                score = silhouette_score(X, labels)
                print(f"k: {k}, silhouette score: {score:.4f}")
                if score > best_score:
                    best_score = score
                    best_k = k
                    improvement = True

            if not improvement:
                no_improve_rounds += 1
            else:
                no_improve_rounds = 0
                last_best_k = best_k

            # Narrow search range
            step = step // 2 if step > 1 else 1
            lower = max(best_k - step, 2)
            upper = best_k + step
            current_range = list(range(lower, upper + 1, step))
        
        return best_k  # Added return statement

    # --- Use the progressive search ---
    best_k = find_best_k_progressively(scaled)

    # --- Final clustering ---
    final_model = KMeans(n_clusters=best_k, random_state=42, n_init="auto")
    final_labels = final_model.fit_predict(scaled)

    return final_labels, data
