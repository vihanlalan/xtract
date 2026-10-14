"""
K-Means Clustering (k=8) on Abyssal Sonar Records
Looks for hidden patterns, clusters, and game tokens in the noise.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

# ── 1. Load ───────────────────────────────────────────────────────────────────
print("Loading data...")
df = pd.read_csv(r"c:\Users\rwerwer\Desktop\Xtract\ml track\abyssal_sonar_records_with_hidden_game_tokens.csv", low_memory=False)
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}\n")

# ── 2. Basic overview ─────────────────────────────────────────────────────────
print("=== COLUMN TYPES ===")
print(df.dtypes)
print()

# Show the 'password' / token column sample
print("=== SAMPLE TOKENS (password column) ===")
print(df['password'].dropna().head(20).tolist())
print()

# ── 3. Select numeric features for clustering ────────────────────────────────
numeric_cols = ['longitude', 'latitude', 'sonar_depth', 'recovery_attempts',
                'artefact_age', 'signal_quality', 'compass_bearing',
                'condition_score', 'weight_kg', 'recovery_distance_km',
                'worth', 'soil_density', 'magnetic_reading']

# Filter to only those that exist and are numeric
available = []
for c in numeric_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')
        available.append(c)

print(f"Features used for clustering: {available}\n")

feat = df[available].copy()
print(f"Missing values per feature:\n{feat.isna().sum()}\n")

# Drop rows with any missing value in features
feat_clean = feat.dropna()
idx_clean = feat_clean.index
print(f"Rows after dropping NaN: {len(feat_clean)} / {len(df)}\n")

# ── 4. Scale ─────────────────────────────────────────────────────────────────
scaler = StandardScaler()
X = scaler.fit_transform(feat_clean)

# ── 5. K-Means k=8 ───────────────────────────────────────────────────────────
print("Running K-Means with k=8 ...")
km = KMeans(n_clusters=8, random_state=42, n_init=20, max_iter=500)
labels = km.fit_predict(X)

sil = silhouette_score(X, labels, sample_size=min(20000, len(X)), random_state=42)
inertia = km.inertia_
print(f"Silhouette Score : {sil:.4f}")
print(f"Inertia          : {inertia:.2f}\n")

# Attach cluster labels back to the full-data subset
df_c = df.loc[idx_clean].copy()
df_c['cluster'] = labels

# ── 6. Cluster summary ────────────────────────────────────────────────────────
print("=== CLUSTER SIZES ===")
print(df_c['cluster'].value_counts().sort_index())
print()

print("=== CLUSTER CENTROIDS (original scale) ===")
centroids = scaler.inverse_transform(km.cluster_centers_)
centroid_df = pd.DataFrame(centroids, columns=available)
centroid_df.index.name = 'cluster'
pd.set_option('display.float_format', '{:.3f}'.format)
pd.set_option('display.max_columns', None)
print(centroid_df.to_string())
print()

# ── 7. Per-cluster feature stats ─────────────────────────────────────────────
print("=== PER-CLUSTER MEAN VALUES ===")
cluster_means = df_c.groupby('cluster')[available].mean()
print(cluster_means.to_string())
print()

# ── 8. Hidden game token analysis ────────────────────────────────────────────
print("=== PASSWORD / TOKEN COLUMN ANALYSIS ===")
tokens = df_c[['cluster', 'password']].copy()
tokens['token_length'] = tokens['password'].astype(str).str.len()
tokens['token_prefix'] = tokens['password'].astype(str).str[:10]

# Count unique tokens per cluster
print("\nUnique tokens per cluster:")
print(tokens.groupby('cluster')['password'].nunique())

# Token prefix patterns per cluster (top 5 per cluster)
print("\nMost common token prefixes per cluster:")
for cl in sorted(tokens['cluster'].unique()):
    top = tokens[tokens['cluster']==cl]['token_prefix'].value_counts().head(5)
    print(f"  Cluster {cl}: {top.to_dict()}")

# Token length distribution
print("\nMean token length per cluster:")
print(tokens.groupby('cluster')['token_length'].mean().round(2))

# ── 9. Categorical feature breakdown per cluster ──────────────────────────────
cat_cols = ['material', 'condition', 'archive_class', 'expedition_zone',
            'inspection_priority', 'sonar_operator']
cat_cols_exist = [c for c in cat_cols if c in df_c.columns]

print(f"\n=== CATEGORICAL BREAKDOWN PER CLUSTER ===")
for col in cat_cols_exist:
    print(f"\n--- {col} ---")
    ct = pd.crosstab(df_c['cluster'], df_c[col], normalize='index').round(3)
    print(ct.to_string())

# ── 10. Notable / extreme records per cluster ─────────────────────────────────
print("\n=== HIGHEST-WORTH RECORDS PER CLUSTER ===")
for cl in sorted(df_c['cluster'].unique()):
    sub = df_c[df_c['cluster']==cl].nlargest(3, 'worth')[['chest_id','worth','password','longitude','latitude','sonar_depth']]
    print(f"\nCluster {cl} – top 3 by worth:")
    print(sub.to_string(index=False))

# ── 11. Outlier / anomaly detection within clusters ──────────────────────────
print("\n=== OUTLIERS (records far from their cluster centroid) ===")
from scipy.spatial.distance import cdist
dists = cdist(X, km.cluster_centers_, metric='euclidean')
df_c['dist_to_centroid'] = dists[np.arange(len(X)), labels]

outliers = df_c.nlargest(20, 'dist_to_centroid')[['chest_id','cluster','dist_to_centroid','worth','password']]
print(outliers.to_string(index=False))

# ── 12. Elbow method – inertia for k=2..12 ───────────────────────────────────
print("\n=== ELBOW CURVE INERTIA (k=2..12) ===")
sample_idx = np.random.RandomState(42).choice(len(X), size=min(30000, len(X)), replace=False)
X_sample = X[sample_idx]
for k in range(2, 13):
    km_tmp = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_sample)
    print(f"  k={k:2d}  inertia={km_tmp.inertia_:.2f}")

# ── 13. PCA for 2-D cluster view (printed as text) ───────────────────────────
print("\n=== PCA 2-D PROJECTION – CLUSTER CENTRES ===")
pca = PCA(n_components=2, random_state=42)
pca.fit(X)
centres_2d = pca.transform(km.cluster_centers_)
print(f"{'Cluster':>8}  {'PC1':>10}  {'PC2':>10}")
for i, (x, y) in enumerate(centres_2d):
    print(f"{i:>8}  {x:>10.4f}  {y:>10.4f}")

print("\n=== VARIANCE EXPLAINED BY PCA COMPONENTS ===")
pca_full = PCA(n_components=min(len(available), 10), random_state=42)
pca_full.fit(X)
for i, v in enumerate(pca_full.explained_variance_ratio_):
    print(f"  PC{i+1}: {v*100:.2f}%")

# ── 14. Save cluster assignments ─────────────────────────────────────────────
out_path = r"c:\Users\rwerwer\Desktop\Xtract\ml track\sonar_clustered_k8.csv"
df_c.to_csv(out_path, index=False)
print(f"\nCluster assignments saved to: {out_path}")

print("\nDone.")
