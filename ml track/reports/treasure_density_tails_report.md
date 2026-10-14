# ⚖️ Lunaris Sector — Treasure Density & Distribution Tails Report

**Dataset:** Lunaris Sector Sub-dataset (`lunaris_sector_records.csv`)  
**Records Analyzed:** 3,381 sonar records  
**Metric:** 
$$\text{Treasure Density} = \frac{\text{Treasure Value (\texttt{worth})}}{\text{Treasure Mass (\texttt{weight\_kg})}}$$

---

## 1. Summary Statistics of Treasure Density

| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| **Count** | 3,381 | 100% valid records (no zero or null masses) |
| **Minimum** | **21.7406** | Heaviest, lowest-value relics ("dead weight") |
| **1st Percentile (P01)** | 122.2548 | Extreme bottom 1% boundary |
| **2nd Percentile (P02)** | **178.2568** | **Lower Tail Boundary** (Bottom 2%) |
| **5th Percentile (P05)** | 282.8091 | Lower decile floor |
| **25th Percentile (Q1)** | 1,152.5023 | First quartile |
| **Median (Q2)** | **2,658.9823** | Typical treasure density in Lunaris |
| **Mean** | 6,530.1143 | Strongly pulled upwards by extreme upper tail |
| **75th Percentile (Q3)** | 6,397.3717 | Third quartile |
| **90th Percentile (P90)** | 15,391.4016 | High density threshold |
| **95th Percentile (P95)** | 24,706.3185 | Top 5% boundary |
| **98th Percentile (P98)** | **42,217.1776** | **Upper Tail Boundary** (Top 2%) |
| **99th Percentile (P99)** | 61,682.5719 | Extreme top 1% boundary |
| **Maximum** | **276,198.0899** | Maximum recorded density |
| **Interquartile Range (IQR)**| 5,244.8694 | $Q3 - Q1$ |
| **Upper IQR Fence** | 14,264.6758 | $Q3 + 1.5 \times \text{IQR}$ (Statistical outliers) |
| **Skewness** | **+7.3566** | Heavily right-skewed power-law distribution |

---

## 2. The Tale of Two Tails: Comparative Analysis

The clue instructs: *"make sense of the tails of the distribution... for the extremes at both ends have stories to tell, not just the upper one."*

| Feature | Upper Tail (Top 2%) | Sector Bulk (Middle 96%) | Lower Tail (Bottom 2%) |
| :--- | :---: | :---: | :---: |
| **Density Range** | **42,217 – 276,198** | 178 – 42,217 | **21.74 – 178.26** |
| **Mean Treasure Density** | **74,628.17** | 5,237.51 | **115.68** |
| **Mean Worth** | 27,445.69 | 5,604.47 | 784.54 |
| **Mean Weight** | **0.414 kg** (414 g) | 1.897 kg | **7.088 kg** |
| **Dominant Materials** | Diamond, Emerald, Ruby, Amethyst | Mixed ores / standard metals | Obsidian, Bronze, Low-grade Jade, Ore |
| **Archive Classification** | **70.6% Protected** | 50.1% Protected | **50.0% Standard / 50.0% Protected** |
| **Narrative / Archetype** | **"Portable Concentrated Riches"** | Standard expedition cargo | **"Heavy Inert Ballast & Coarse Relics"** |

### Upper Extreme Tail (Top 2% — 68 Records)
- **Story:** High-purity, ultra-concentrated jewels and precious artefacts. Tiny mass (often under 300 grams), yet valued upwards of 20,000–84,000 credits. Heavily secured with `protected` archive class status.
- **Top Record:** `CH-0082462` — Density: **276,198.09**, Worth: **24,581.63**, Mass: **0.089 kg** (Ruby, protected).

### Lower Extreme Tail (Bottom 2% — 68 Records)
- **Story:** Extremely heavy, dense stone/metal masses with disproportionately negligible worth. Bulky relics, ballast stones, coarse obsidian, or degraded bronze anchors.
- **Lowest Record:** `CH-0123086` — Density: **21.74**, Worth: **156.38**, Mass: **7.193 kg** (Pearl, protected).

---

## 3. Sample Records from Isolated Tails

### Top 5 Upper Density Records (Highest $\text{Worth} / \text{Weight}$)
| Chest ID | Treasure Density | Worth | Weight (kg) | Material | Archive Class | Password Token |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `CH-0082462` | 276,198.09 | 24,581.63 | 0.089 | Ruby | protected | `TR--jH5COeFg5JG6pfhLK6TwkHsK8I2GNk_` |
| `CH-0091225` | 164,665.77 | 62,243.66 | 0.378 | Emerald | protected | `TR-tWrxS69Kk9coEM417l53OZGrqtRBrHqq` |
| `CH-0114417` | 164,095.14 | 84,016.71 | 0.512 | Emerald | protected | `TR-eYUMk1hRYRj4jQ0qOtSdjkhoM3Qumuy1` |
| `CH-0033540` | 156,277.00 | 40,632.02 | 0.260 | Diamond | protected | `TR-LSOb5Hr_fMBEUeOX9bBSTrxwe-El4Aar` |
| `CH-0082278` | 150,009.63 | 24,001.54 | 0.160 | Amethyst | protected | `TR-rZR7H0F3U_u1zovWX8rUorYDY6jIJRV7` |

### Bottom 5 Lower Density Records (Lowest $\text{Worth} / \text{Weight}$)
| Chest ID | Treasure Density | Worth | Weight (kg) | Material | Archive Class | Password Token |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `CH-0123086` | 21.74 | 156.38 | 7.193 | Pearl | protected | `TR-sn59ah7_HiXuNCcIXk22ybfdLTE7ppqx` |
| `CH-0074720` | 26.63 | 143.47 | 5.388 | Obsidian | standard | `TR-NjOUifEFMpEWrnWQiYZcNj9NZjbsmQwS` |
| `CH-0006638` | 32.44 | 393.89 | 12.141 | Bronze | protected | `TR-EmPjU1TJRFUXcZg7aCZFxNG3S9EmfgBx` |
| `CH-0115552` | 39.40 | 275.16 | 6.983 | Bronze | protected | `TR-7WW9MvL8rQ0ulQUlstMD1hcIV37WZnmz` |
| `CH-0057016` | 39.47 | 537.20 | 13.611 | Amethyst | protected | `TR-CM6oemotgiyoGnXVEZvKhh0jb0L_Qf-5` |

---

## 4. Isolated Datasets Generated

The filtered datasets have been written directly to the workspace:
1. [`lunaris_with_density.csv`](file:///c:/Users/rwerwer/Desktop/Xtract/ml%20track/lunaris_with_density.csv) (3,381 rows): Full Lunaris sector data with `treasure_density` computed.
2. [`lunaris_upper_density_tail.csv`](file:///c:/Users/rwerwer/Desktop/Xtract/ml%20track/lunaris_upper_density_tail.csv) (68 rows): Top 2% density tail ($\ge 42,217.18$).
3. [`lunaris_lower_density_tail.csv`](file:///c:/Users/rwerwer/Desktop/Xtract/ml%20track/lunaris_lower_density_tail.csv) (68 rows): Bottom 2% density tail ($\le 178.26$).
4. [`lunaris_density_extreme_tails.csv`](file:///c:/Users/rwerwer/Desktop/Xtract/ml%20track/lunaris_density_extreme_tails.csv) (136 rows): Combined extreme tails tagged with `tail` (`UPPER` / `LOWER`).
