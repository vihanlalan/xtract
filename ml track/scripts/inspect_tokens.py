"""
Decode analysis for Step 6 / Final Stage:
Investigate survivors of the blind spot, N=8, N^2=64, base-64 decoding, password tokens, and coordinates leading to Rue.
"""

import base64
import pandas as pd
import numpy as np

# Load full Lunaris with density
df_lunaris = pd.read_csv('lunaris_with_density.csv')
print(f"Total Lunaris records: {len(df_lunaris)}")

# Load extreme tails if relevant
df_tails = pd.read_csv('lunaris_density_extreme_tails.csv')
print(f"Tails records: {len(df_tails)}")

# Check passwords in tails
print("\nSample passwords in upper tail:")
for p in df_tails[df_tails['tail'] == 'UPPER']['password'].head(10):
    print(p)

print("\nSample passwords in lower tail:")
for p in df_tails[df_tails['tail'] == 'LOWER']['password'].head(10):
    print(p)
