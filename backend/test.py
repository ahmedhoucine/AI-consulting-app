import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Load your data
data = pd.read_csv("data.csv")

# Quick check
print(data.info())          # See column types and missing values
print(data.isna().sum())    # Count of NaNs per column

# Drop columns that are completely empty
data = data.dropna(axis=1, how='all')

# Optional: Fill remaining NaNs
imputer = SimpleImputer(strategy='median')
data_imputed = imputer.fit_transform(data)

# Scale
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_imputed)

print("Processed data shape:", data_scaled.shape)
