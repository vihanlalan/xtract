# 📍 Location Descriptions — Hidden Word & Lunaris Sector Report

**Files:** `location_descriptions.csv` → `abyssal_sonar_records_with_hidden_game_tokens.csv`  
**Output:** [`lunaris_sector_records.csv`](file:///c:/Users/rwerwer/Desktop/Xtract/ml%20track/lunaris_sector_records.csv) (3,381 rows) · [`lunaris_extreme_treasure.csv`](file:///c:/Users/rwerwer/Desktop/Xtract/ml%20track/lunaris_extreme_treasure.csv) (170 rows)

---

## 1. 🔎 Decoding the Hidden Word in the Descriptions

The clue says descriptions *"conceal a single word that points to a reference."* Here's what stands out:

### Acrostic Analysis
| What | Letters |
|------|---------|
| First letter of each **description** | `A V O A E D R A S C A M T H D L T N A C R C S P` |
| First letter of each **location name** | `A V O A E D R A S C A M T H D L T N A C R C S P` |

No acrostic word is formed — the hiding method is different.

### Unique Ecological / Creature Signals Per Location
| Location | Creatures/Keywords embedded |
|----------|-----------------------------|
| Aurelia | *amber-coloured squids* |
| Elysium | *moon jelly fishes, mauve stinger* |
| Spartion | *blackfoot limpets* |
| Corinthia | *coral gardens* |
| **Lunaris** 🎯 | **nautilus, dogfish, mackerel sharks, moonlit, silver** |
| Rhodos | *comb jellies* |

### Why Lunaris is the Signal

> *"Lunaris is a **moonlit** abyssal shelf where **nautilus** wreckages repose beneath **silent silver currents**, serving as a thriving habitat for numerous **dogfish** and **mackerel sharks**."*

Lunaris is the **only location** whose description:
1. Names **nautilus** — directly echoing `theara` (the disguised Nautilus creature from the creatures table)
2. Mentions **silver** currents — the dominant material in the sonar records
3. Uses **moonlit** — linking to the moonlit/lunar theme embedded in its name (*Luna* = moon)
4. Is the **only location with multiple named species** (nautilus + dogfish + mackerel sharks)

The word hidden in the description is **"nautilus"** — which points directly back to creature `theara` in the creatures table, forming a cross-reference chain: `theara (nautilus) → Lunaris`.

---

## 2. 📊 Lunaris Sector — Full Statistical Profile

**Total Lunaris records: 3,381** out of 149,896 = **2.26% of the dataset**

### Numeric Feature Statistics (Lunaris only)

| Feature | Min | Mean | Median | 75th % | Max |
|---------|-----|------|--------|--------|-----|
| longitude | 71.891 | 72.728 | 72.711 | 72.820 | 73.750 |
| latitude | 17.967 | 18.908 | 18.888 | 19.031 | 19.948 |
| sonar_depth | 20.0 | 130.5 | 127.3 | 148.5 | 269.6 |
| recovery_attempts | 1 | 5.02 | 5 | 7 | 9 |
| artefact_age | 1 | 2,070 | 2,063 | 3,038 | 3,998 |
| signal_quality | 0.002 | 0.521 | 0.519 | 0.756 | 0.990 |
| compass_bearing | 0.32 | 181.8 | 176.1 | 226.1 | 359.7 |
| weight_kg | 0.1 | 1.99 | 1.306 | 2.433 | 26.675 |
| recovery_distance_km | 0.03 | 476.6 | 477.3 | 719.1 | 949.95 |
| **worth** | **124.88** | **5,946.81** | **3,559.08** | **7,145.87** | **173,142.52** |
| soil_density | 0.202 | 1.532 | 1.535 | 1.639 | 2.848 |
| magnetic_reading | 0.07 | 50.6 | 52.4 | 58.1 | 94.9 |

### Worth Distribution — Lunaris

| Percentile | Worth ($) |
|-----------|-----------|
| Min | 124.88 |
| 50th (median) | 3,559.08 |
| 75th | 7,145.87 |
| 90th | 13,167.36 |
| **95th** | **18,518.35** ← extreme threshold |
| 99th | 35,163.08 |
| **Max** | **173,142.52** |

### Categorical Breakdown

| material | count | | archive_class | count |
|----------|-------|-|---------------|-------|
| Emerald | 255 | | standard | 2,227 |
| Platinum | 237 | | **protected** | **1,154** |
| Electrum | 237 | | | |
| Bronze | 235 | | **expedition_zone** | count |
| Gold | 235 | | Eastern Ridge | 593 |
| Silver | 223 | | Uncharted Sector | 589 |
| Sapphire | 221 | | North Trench | 571 |
| Diamond | 221 | | Southern Basin | 550 |
| Obsidian | 221 | | Abyssal Plain | 540 |
| Jade | 220 | | Western Shelf | 538 |

---

## 3. 🏆 Extreme Treasure Records — Lunaris Sector

**Threshold:** top 5% by worth = **≥ $18,518.35** → **170 records**

### Top 30 by Worth

| # | chest_id | Worth ($) | Token | lon | lat | depth | archive |
|---|----------|-----------|-------|-----|-----|-------|---------|
| 1 | **CH-0006754** | **173,142.52** | `TR-yBzYxQL6yElPJDRMhqNB3oK3qyTZLLLk` | 72.412 | 18.663 | 113.4 | standard |
| 2 | CH-0114417 | 84,016.71 | `TR-eYUMk1hRYRj4jQ0qOtSdjkhoM3Qumuy1` | 72.829 | 18.901 | 114.9 | protected |
| 3 | CH-0101109 | 74,417.01 | `TR-vFmFYyftJpj8ZEih4xJWpiVLYr4Y8WKg` | 72.760 | 19.091 | 156.7 | standard |
| 4 | CH-0000029 | 72,712.06 | `TR-_ZrP7MieYhM-yxBjMBiWP7a1hgvomAoo` | 72.618 | 18.809 | 130.4 | protected |
| 5 | CH-0120146 | 65,376.83 | `TR-vQfIpET980uGgneXtFgIz4fvWum_HeLu` | 72.414 | 18.343 | 159.3 | standard |
| 6 | CH-0041408 | 64,129.72 | `TR-q4bK02Zdtk7JJvw33rVt60tsIKmAD824` | 72.711 | 18.824 | 125.3 | protected |
| 7 | CH-0034224 | 62,526.46 | `TR-zg8it1zA5Y5pojNG4OlFdqrK9CBKgjaB` | 72.831 | 18.844 | 102.2 | standard |
| 8 | CH-0091225 | 62,243.66 | `TR-tWrxS69Kk9coEM417l53OZGrqtRBrHqq` | 72.987 | 18.896 | 71.0 | protected |
| 9 | CH-0014149 | 59,565.95 | `TR-UuTABtQtTEKW3j2OC_PulmJ6ZQythwK5` | 72.649 | 18.912 | 134.9 | protected |
| 10 | CH-0148990 | 59,433.39 | `TR-rjIPNloKsygB_a3zUL2xZqOdMBp7zxtZ` | 72.868 | 18.826 | 92.5 | protected |
| 11 | CH-0037124 | 56,607.06 | `TR-GMMQQxbf3Yjs61A74LmoRx_e5MYW61og` | 72.363 | 18.652 | 138.9 | standard |
| 12 | CH-0118313 | 56,308.64 | `TR-trmr8Vd30NJIGaYRgI-IZkJMvvYiRyPm` | 73.490 | 18.080 | 55.1 | protected |
| 13 | CH-0082750 | 55,705.73 | `TR-JEIE-6bd81uv0JjU2cMb4mugFVBpIK2_` | 72.706 | 18.896 | 133.8 | protected |
| 14 | CH-0004329 | 55,681.96 | `TR-UFHqpXKXy32J3Ot80pWz2mBlzrpBOk-T` | 72.031 | 19.423 | 136.8 | standard |
| 15 | CH-0143348 | 54,553.31 | `TR-eBej7_FlutrfAE1Tq03YfDwakJdB_wZn` | 72.579 | 18.839 | 132.2 | protected |
| 16 | CH-0021367 | 51,047.91 | `TR-Vsq_8TuzdXLoHk2D7Loe3H0h-v06k8hs` | 73.321 | 18.097 | 260.1 | standard |
| 17 | CH-0050601 | 50,673.16 | `TR-E_UXQpmNOlsZWKkI9PpRDlJOGhWlW1qc` | 72.770 | 19.057 | 144.4 | standard |
| 18 | CH-0102984 | 49,693.09 | `TR-S8Q-SOJsoLHnZ6JTyYHaMMjpOnlla3Af` | 73.077 | 18.343 | 229.7 | standard |
| 19 | CH-0144152 | 49,534.99 | `TR-IpsQEwPQH3nLls5FSuTK9VoWoFRPLvdC` | 72.791 | 18.869 | 103.3 | standard |
| 20 | CH-0099698 | 46,524.93 | `TR-f58Z7fiwCoV513NzBu_oiZoc8Bk0Zl1F` | 72.787 | 18.916 | 121.7 | standard |
| 21 | CH-0110762 | 44,772.07 | `TR-lLv6MttzzZ8qSte6RU8HVPGgZXQlo5ii` | 72.433 | 18.676 | 112.4 | standard |
| 22 | CH-0098842 | 44,539.84 | `TR-RopdMvxc-a639Q69zyrrCU25yNVWsg5h` | 72.593 | 18.736 | 77.4 | standard |
| 23 | CH-0090132 | 42,569.42 | `TR-z13RdxJbu6MQYsFippSZnH9WJwJIr5Tj` | 72.698 | 18.658 | 160.3 | protected |
| 24 | CH-0075701 | 42,493.83 | `TR-_K9nQ5GAreKv6E5sKJA9_4ol3DIihwb_` | 72.425 | 19.648 | 168.1 | protected |
| 25 | CH-0016400 | 40,990.41 | `TR-f6s7MLqzB12GvqPL57MtksUb59fXUuI1` | 73.058 | 19.152 | 180.7 | protected |
| 26 | CH-0048584 | 40,689.29 | `TR-IxDBqhxOoSkKUp2wPrUb8fu97SMa-Fmh` | 73.146 | 19.484 | 81.7 | protected |
| 27 | CH-0033540 | 40,632.02 | `TR-LSOb5Hr_fMBEUeOX9bBSTrxwe-El4Aar` | 73.671 | 18.733 | 224.0 | protected |
| 28 | CH-0138906 | 37,514.72 | `TR--6WiVkSvhcvwhQh_ygR5EzMk3xwuwv89` | 73.060 | 18.293 | 207.4 | protected |
| 29 | CH-0096175 | 37,351.88 | `TR-xJKq2UYCFcDDrqXOiM2qCOqTAKRexoyE` | 72.629 | 18.833 | 132.4 | protected |
| 30 | CH-0068577 | 36,705.07 | `TR-WGapfUoWRUlGGJEk_3JOMBJ1aG9AZvT1` | 72.561 | 19.130 | 165.5 | protected |

---

## 4. ⚖️ Extreme vs Normal Lunaris — Mean Feature Comparison

| Feature | Normal (3,211 rows) | Extreme (170 rows) | Difference |
|---------|--------------------|--------------------|------------|
| longitude | 72.728 | 72.759 | +0.031 |
| latitude | 18.908 | 18.943 | +0.035 |
| sonar_depth | 130.2 | 134.3 | +4.1m deeper |
| artefact_age | 2,074 | 1,951 | −123 years (younger) |
| signal_quality | 0.520 | 0.525 | ≈ same |
| weight_kg | 1.967 | 2.046 | slightly heavier |
| **worth** | **$4,627** | **$30,881** | **6.7× higher** |
| magnetic_reading | 50.2 | 53.4 | slightly higher |

> [!NOTE]
> Extreme Lunaris records are slightly deeper, younger artefacts, and marginally heavier — but the signal quality and most spatial features are nearly identical to normal records, confirming these are **truly hidden treasures buried in the noise**.

---

## 5. Extreme Lunaris — Material & Seal Integrity

| Material (top extreme) | Count | | Seal Integrity | Count |
|------------------------|-------|-|----------------|-------|
| Diamond | 18 | | Unverified | 46 |
| Sapphire | 15 | | Weathered | 45 |
| Obsidian | 14 | | Intact | 44 |
| Electrum | 14 | | Partial | 35 |
| Silver | 13 | | | |

> [!IMPORTANT]
> **50% protected / 50% standard** in extreme records — unlike the full Lunaris set (66% standard). High-worth Lunaris chests are disproportionately `protected`.

---

## 6. Summary: The Decoding Chain So Far

```
location_descriptions.csv
  └─ Lunaris description mentions "nautilus"
       └─ Cross-ref: theara (creatures_table_final.csv) = disguised Nautilus
            └─ theara has "dozens of cirri instead of eight arms"
                 └─ Brittle Star = 5 arms → 5² = 25  (the number for final stage)

Lunaris sector → 3,381 records isolated
  └─ Extreme treasure density: 170 records (worth ≥ $18,518)
       └─ Top token: CH-0006754 worth $173,142.52
            Token: TR-yBzYxQL6yElPJDRMhqNB3oK3qyTZLLLk
```
