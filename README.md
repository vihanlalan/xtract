# 🌊 Xtract — Code Repository & Analysis Pipelines

A comprehensive analytical, reverse-engineering, and machine learning framework for the **Xtract** challenge across all competition tracks:
- **ML Track:** Sonar clustering, abyssal creature anatomy decoding, Lunaris sector isolation, treasure density distribution analysis, signal hardening/classification, and final survivor coordinate extraction.
- **DS Track 1:** Capsule inspection, trace analysis, and bridge editor configs.
- **DS Track 4:** Ledger analysis, night readouts, and vault monitoring.

---

## 📁 Repository Structure

```
.
├── ds track 1/                          # Data Science Track 1: Capsule inspection & tools
│   ├── bridge/                         # Standard loads and trace channel configs
│   ├── capsules/                       # Capsules A, B, and C JSON data
│   ├── selftest/                       # Self-test capsule and expected values
│   ├── standards/                      # Exposure reference standards
│   ├── open_capsule.py                 # Tool for inspecting and unpacking capsules
│   └── README.md
│
├── ds track 4/                          # Data Science Track 4: Financial ledgers and vault telemetry
│   ├── ledger.csv
│   ├── night_readouts.csv
│   └── vault_readings.csv
│
├── ml track/                            # Machine Learning Track
│   ├── scripts/                        # All core analysis, modeling, and decoding pipelines
│   │   ├── cluster_sonar.py            # Step 1: K-Means (k=8) sonar clustering
│   │   ├── parse_creatures.py          # Step 2: Creature anatomy parser
│   │   ├── full_creature_anatomy.py    # Step 2: Deep creature structure & limb catalog
│   │   ├── lunaris_analysis.py         # Step 3: Hidden reference word & Lunaris sector filter
│   │   ├── treasure_density.py         # Step 4: Treasure density distribution & tail analysis
│   │   ├── train_signal_classifiers.py # Step 5: 8-model classification benchmark & signal hardening
│   │   └── inspect_tokens.py           # Step 6: Token inspection and coordinate extraction
│   │
│   ├── reports/                        # Detailed technical documentation artifacts
│   │   ├── sonar_clustering_report.md
│   │   ├── creatures_anatomy_report.md
│   │   ├── lunaris_sector_report.md
│   │   ├── treasure_density_tails_report.md
│   │   ├── model_classification_comparison_report.md
│   │   └── path_to_rue_final_report.md
│   │
│   ├── location_descriptions.csv       # Sector descriptions and ecological profiles
│   ├── creatures_table_final.csv       # Master creature anatomy and traits table
│   ├── sonic_script.js                 # Sonic archives client-side engine and puzzle logic
│   ├── model_comparison_results.csv    # Test set metrics across all 8 classification models
│   ├── model_cross_validation_results.csv # 5-Fold cross-validation benchmark
│   ├── feature_importance_gradient_boosting.csv
│   └── feature_importance_random_forest.csv
│
├── .gitignore                          # Clean repository hygiene (excludes huge raw binary blobs)
└── README.md
```

---

## 🚀 ML Track Workflow & Pipeline Execution

### Step 1: Cluster the Sonar Signals ($k = 8$)
```bash
python "ml track/scripts/cluster_sonar.py"
```
- Clusters abyssal sonar records into 8 main current streams using coordinate, signal, and magnetic features.

### Step 2: Creature Anatomy & Appendage Analysis
```bash
python "ml track/scripts/full_creature_anatomy.py"
```
- Evaluates all 57 abyssal creatures. Identifies Argonaut (8 arms, disguised as a nautilus) and calculates $N = 8 \implies N^2 = 64$.

### Step 3: Location Clue & Lunaris Sector Isolation
```bash
python "ml track/scripts/lunaris_analysis.py"
```
- Decodes hidden textual reference to `"nautilus"` in `location_descriptions.csv`, subsetting to the 3,381 records of the **Lunaris sector**.

### Step 4: Treasure Density & Distribution Tails
```bash
python "ml track/scripts/treasure_density.py"
```
- Computes $\text{Treasure Density} = \frac{\text{Worth}}{\text{Weight (kg)}}$.
- Isolates upper 2% (compact valuables, high density) and lower 2% (heavy ballast relics, low density).

### Step 5: Harden & Classify Signals (Model Comparison)
```bash
python "ml track/scripts/train_signal_classifiers.py"
```
- Trains and benchmarks 8 distinct ML classifiers to eliminate the Capitol's blind spot (misclassifying `protected` rebel signals as `standard` background noise).
- Models compared: Logistic Regression, Random Forest, Gradient Boosting, HistGradientBoosting, Support Vector Machine, Extra Trees, K-Nearest Neighbors, and MLP Neural Network.
- Demonstrates that `treasure_density` is the #1 most important feature in Gradient Boosting (28.4% importance).

### Step 6: Final Survivor Consensus & Path to Rue
```bash
python "ml track/scripts/inspect_tokens.py"
```
- Enforces unanimous model consensus ("tight circle of allies") to isolate the top 29 infallible protected signals.
- Computes focal coordinates: **18.9262° N, 72.8697° E**.
- Unlocks the Gamemaker Sonic Archives reveal: **`BACKSTAIRS LIFT`** (*"The gamemakers await you there"*).
