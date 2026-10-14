"""
Treasure Density Analysis for Lunaris Sector
Treasure Density = worth / weight_kg
Examine BOTH tails: ultra-high density AND ultra-low density
"""

import pandas as pd
import numpy as np

# ── Load Lunaris records ──────────────────────────────────────────────────────
print("Loading Lunaris sector records...")
df = pd.read_csv('lunaris_sector_records.csv', low_memory=False)
print(f"Rows: {len(df)}")

# ── Numeric coercion ──────────────────────────────────────────────────────────
df['worth']     = pd.to_numeric(df['worth'],     errors='coerce')
df['weight_kg'] = pd.to_numeric(df['weight_kg'], errors='coerce')

# Drop rows where either value is missing or weight is zero (div by zero)
before = len(df)
df = df.dropna(subset=['worth', 'weight_kg'])
df = df[df['weight_kg'] > 0]
print(f"Usable rows (non-null, weight>0): {len(df)}  (dropped {before - len(df)})")

# ── Compute Treasure Density ──────────────────────────────────────────────────
df['treasure_density'] = df['worth'] / df['weight_kg']

print("\n" + "=" * 90)
print("TREASURE DENSITY DISTRIBUTION  (worth / weight_kg)")
print("=" * 90)

td = df['treasure_density']
print(f"\n  Count        : {len(td):,}")
print(f"  Min          : {td.min():.4f}")
print(f"  1st  pct     : {td.quantile(0.01):.4f}")
print(f"  2nd  pct     : {td.quantile(0.02):.4f}")
print(f"  5th  pct     : {td.quantile(0.05):.4f}")
print(f"  10th pct     : {td.quantile(0.10):.4f}")
print(f"  25th pct     : {td.quantile(0.25):.4f}")
print(f"  Median       : {td.median():.4f}")
print(f"  Mean         : {td.mean():.4f}")
print(f"  75th pct     : {td.quantile(0.75):.4f}")
print(f"  90th pct     : {td.quantile(0.90):.4f}")
print(f"  95th pct     : {td.quantile(0.95):.4f}")
print(f"  98th pct     : {td.quantile(0.98):.4f}")
print(f"  99th pct     : {td.quantile(0.99):.4f}")
print(f"  Max          : {td.max():.4f}")
print(f"  Std Dev      : {td.std():.4f}")
print(f"  Skewness     : {td.skew():.4f}")

# IQR-based outlier thresholds
Q1  = td.quantile(0.25)
Q3  = td.quantile(0.75)
IQR = Q3 - Q1
lower_iqr = Q1 - 1.5 * IQR
upper_iqr = Q3 + 1.5 * IQR
print(f"\n  IQR          : {IQR:.4f}")
print(f"  Lower fence (Q1 - 1.5×IQR) : {lower_iqr:.4f}")
print(f"  Upper fence (Q3 + 1.5×IQR) : {upper_iqr:.4f}")

# ── Tail definitions ──────────────────────────────────────────────────────────
p02 = td.quantile(0.02)
p98 = td.quantile(0.98)
p05 = td.quantile(0.05)
p95 = td.quantile(0.95)

lower_tail = df[df['treasure_density'] <= p02].copy()
upper_tail = df[df['treasure_density'] >= p98].copy()

print("\n" + "="*90)
print("TAIL ISOLATION  (bottom 2% and top 2%)")
print("="*90)
print(f"  Bottom 2% threshold : density <= {p02:.4f}  ->  {len(lower_tail)} records")
print(f"  Top    2% threshold : density >= {p98:.4f}  ->  {len(upper_tail)} records")

# ── Columns to display ────────────────────────────────────────────────────────
show_cols = ['chest_id', 'treasure_density', 'worth', 'weight_kg',
             'sonar_depth', 'signal_quality', 'compass_bearing',
             'magnetic_reading', 'longitude', 'latitude',
             'archive_class', 'material', 'seal_integrity',
             'condition_score', 'password']

# ── UPPER TAIL (extremely HIGH density — light but very valuable) ─────────────
print(f"\n{'='*90}")
print("UPPER TAIL — HIGHEST TREASURE DENSITY (top 2%)")
print("Light artefacts, disproportionately high worth → 'most precious per gram'")
print(f"{'='*90}")
upper_sorted = upper_tail.sort_values('treasure_density', ascending=False)
print(upper_sorted[show_cols].head(40).to_string(index=False))

# ── LOWER TAIL (extremely LOW density — heavy but low value) ─────────────────
print(f"\n{'='*90}")
print("LOWER TAIL — LOWEST TREASURE DENSITY (bottom 2%)")
print("Heavy artefacts, disproportionately low worth → 'near-worthless rocks'")
print(f"{'='*90}")
lower_sorted = lower_tail.sort_values('treasure_density', ascending=True)
print(lower_sorted[show_cols].head(40).to_string(index=False))

# ── Stats: upper vs lower tail comparison ────────────────────────────────────
print(f"\n{'='*90}")
print("COMPARISON: UPPER TAIL vs LOWER TAIL vs BULK")
print(f"{'='*90}")
num_cols = ['treasure_density', 'worth', 'weight_kg', 'sonar_depth',
            'signal_quality', 'compass_bearing', 'magnetic_reading',
            'condition_score', 'artefact_age', 'recovery_distance_km']
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')
    
bulk = df[(df['treasure_density'] > p02) & (df['treasure_density'] < p98)]
print(f"\n{'Feature':<25} {'Upper tail':>14} {'Bulk':>14} {'Lower tail':>14}")
print("-" * 70)
for c in num_cols:
    u = upper_tail[c].mean()
    b = bulk[c].mean()
    l = lower_tail[c].mean()
    print(f"{c:<25} {u:>14.3f} {b:>14.3f} {l:>14.3f}")

# ── Categorical breakdown of tails ───────────────────────────────────────────
print(f"\n{'='*90}")
print("CATEGORICAL PROFILE OF TAILS")
print(f"{'='*90}")

for col in ['material', 'archive_class', 'seal_integrity', 'condition_score']:
    if col in df.columns:
        print(f"\n--- {col} ---")
        print(f"  UPPER tail:\n{upper_tail[col].value_counts().head(8).to_string()}")
        print(f"  LOWER tail:\n{lower_tail[col].value_counts().head(8).to_string()}")

# ── Combined extreme records ──────────────────────────────────────────────────
upper_tail['tail'] = 'UPPER'
lower_tail['tail'] = 'LOWER'
combined_tails = pd.concat([upper_tail, lower_tail]).sort_values('treasure_density', ascending=False)

# ── Save outputs ──────────────────────────────────────────────────────────────
df.to_csv('lunaris_with_density.csv', index=False)
upper_sorted.to_csv('lunaris_upper_density_tail.csv', index=False)
lower_sorted.to_csv('lunaris_lower_density_tail.csv', index=False)
combined_tails.to_csv('lunaris_density_extreme_tails.csv', index=False)

print(f"\nSaved:")
print(f"  lunaris_with_density.csv            ({len(df):,} rows)")
print(f"  lunaris_upper_density_tail.csv       ({len(upper_sorted):,} rows)")
print(f"  lunaris_lower_density_tail.csv       ({len(lower_sorted):,} rows)")
print(f"  lunaris_density_extreme_tails.csv    ({len(combined_tails):,} rows)")
print("\nDone.")
