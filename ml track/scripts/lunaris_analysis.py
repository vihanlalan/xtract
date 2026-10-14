"""
Step 1: Decode the hidden word in location_descriptions.csv
Step 2: Filter sonar records for location_name == 'Lunaris'
Step 3: Extract extreme treasure density (high-worth) records
Step 4: Full statistical profile of the Lunaris sector
"""

import csv, re, pandas as pd, numpy as np

# ── 1. Print all descriptions with acrostic / hidden-word analysis ────────────
print("=" * 100)
print("LOCATION DESCRIPTIONS — HIDDEN WORD ANALYSIS")
print("=" * 100)

locations = []
with open('location_descriptions.csv', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        name = row['location_name'].strip()
        desc = row['location_description'].strip()
        if name:
            locations.append((name, desc))

# --- First-letter acrostic across all descriptions (in file order) ---
first_letters = ''.join(d[0] for _, d in locations)
print(f"\nFirst letter of each description (acrostic): {first_letters}")

# --- First letter of each location name ---
name_letters = ''.join(n[0] for n, _ in locations)
print(f"First letter of each location name        : {name_letters}")

# --- Lunaris description in detail ---
print("\n--- Lunaris Description (verbatim) ---")
for name, desc in locations:
    if name == 'Lunaris':
        print(f"  {desc}")
        words = desc.split()
        print(f"\n  Word count : {len(words)}")
        print(f"  Words      : {words}")
        # First letter of each word
        initials = ''.join(w[0] for w in words if w[0].isalpha())
        print(f"  Word initials: {initials}")

# --- Look for unusual/unique keywords in each description ---
print("\n--- Unique/Standout Words per Description ---")
for name, desc in locations:
    # Find capitalised mid-sentence words or numbers
    caps = re.findall(r'\b[A-Z][a-z]{3,}\b', desc[desc.index(' '):])  # skip first word
    nums = re.findall(r'\b\d+\b', desc)
    animals = re.findall(r'\b(shark|jelly|octopus|squid|nautilus|eel|fish|crab|lobster|limpet|manta|whale|dolphin|mackerel|dogfish|eel|ray)\b', desc.lower())
    if caps or nums or animals:
        print(f"  {name:<14}: caps={caps}  nums={nums}  creatures={animals}")

# ── 2. Load full sonar dataset ────────────────────────────────────────────────
print("\n" + "=" * 100)
print("FILTERING SONAR RECORDS FOR LUNARIS SECTOR")
print("=" * 100)

df = pd.read_csv('abyssal_sonar_records_with_hidden_game_tokens.csv', low_memory=False)
print(f"\nFull dataset shape: {df.shape}")

# Unique location names
print(f"\nAll location_name values in sonar data:")
print(df['location_name'].value_counts().to_string())

# ── 3. Isolate Lunaris ────────────────────────────────────────────────────────
lunaris = df[df['location_name'] == 'Lunaris'].copy()
print(f"\n{'='*60}")
print(f"Lunaris records: {len(lunaris)} rows  ({len(lunaris)/len(df)*100:.2f}% of total)")
print(f"{'='*60}")

# ── 4. Numeric conversion ─────────────────────────────────────────────────────
num_cols = ['longitude','latitude','sonar_depth','recovery_attempts','artefact_age',
            'signal_quality','compass_bearing','condition_score','weight_kg',
            'recovery_distance_km','worth','soil_density','magnetic_reading']
for c in num_cols:
    lunaris[c] = pd.to_numeric(lunaris[c], errors='coerce')

# ── 5. General stats ──────────────────────────────────────────────────────────
print("\n--- LUNARIS: Descriptive Statistics ---")
print(lunaris[num_cols].describe().round(3).to_string())

# ── 6. Extreme treasure density — high worth records ─────────────────────────
print("\n--- LUNARIS: Worth Distribution ---")
worth = lunaris['worth'].dropna()
print(f"  Min     : {worth.min():.2f}")
print(f"  Mean    : {worth.mean():.2f}")
print(f"  Median  : {worth.median():.2f}")
print(f"  75th %  : {worth.quantile(0.75):.2f}")
print(f"  90th %  : {worth.quantile(0.90):.2f}")
print(f"  95th %  : {worth.quantile(0.95):.2f}")
print(f"  99th %  : {worth.quantile(0.99):.2f}")
print(f"  Max     : {worth.max():.2f}")

# --- Define extreme threshold: top 5% worth ---
thresh_95 = worth.quantile(0.95)
extreme = lunaris[lunaris['worth'] >= thresh_95].copy()
print(f"\n--- LUNARIS EXTREME TREASURE (worth >= 95th percentile = {thresh_95:.2f}) ---")
print(f"  Records: {len(extreme)}")

extreme_sorted = extreme.sort_values('worth', ascending=False)
print("\nTop 30 extreme Lunaris treasure records:")
cols_show = ['chest_id','worth','password','longitude','latitude','sonar_depth',
             'signal_quality','compass_bearing','magnetic_reading','archive_class']
print(extreme_sorted[cols_show].head(30).to_string(index=False))

# ── 7. Categorical breakdown ──────────────────────────────────────────────────
print("\n--- LUNARIS: Categorical Breakdown ---")
for col in ['material','condition','archive_class','inspection_priority','sonar_operator','expedition_zone']:
    if col in lunaris.columns:
        print(f"\n  {col}:")
        print(lunaris[col].value_counts().to_string())

# ── 8. Extreme vs non-extreme comparison ─────────────────────────────────────
print("\n--- EXTREME vs NORMAL Lunaris records (mean values) ---")
lunaris['is_extreme'] = lunaris['worth'] >= thresh_95
compare = lunaris.groupby('is_extreme')[num_cols].mean().round(3)
compare.index = ['Normal', 'Extreme']
print(compare.to_string())

# ── 9. Archive class breakdown in extreme records ─────────────────────────────
print("\n--- EXTREME LUNARIS: archive_class ---")
print(extreme['archive_class'].value_counts())
print("\n--- EXTREME LUNARIS: material ---")
print(extreme['material'].value_counts().head(10))
print("\n--- EXTREME LUNARIS: seal_integrity ---")
if 'seal_integrity' in extreme.columns:
    print(extreme['seal_integrity'].value_counts())

# ── 10. Save Lunaris subset ───────────────────────────────────────────────────
out_path = r'lunaris_sector_records.csv'
lunaris.to_csv(out_path, index=False)
print(f"\nLunaris records saved to: {out_path}  ({len(lunaris)} rows)")

extreme_out = r'lunaris_extreme_treasure.csv'
extreme_sorted.to_csv(extreme_out, index=False)
print(f"Extreme Lunaris records saved to: {extreme_out}  ({len(extreme_sorted)} rows)")

print("\nDone.")
