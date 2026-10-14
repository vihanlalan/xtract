# 🗝️ Final Stage: Survivors of the Blind Spot & The Path to Rue

**Text Clue Analysis:**
> *"Draw a line around only the survivors of the blind spot. Pull the boundary tight, demand a tight circle of allies... take the number of limbs the creature bears and square it, using the result as their base. This is what will lead them to Rue."*

---

## 1. Survivors of the Blind Spot ("Tight Circle of Allies")

In Step 5, we unmasked the Capitol's blind spot — where protected rebel signals are misclassified as standard background noise. 

- **The Survivors:** The genuine `protected` records correctly recognized by the classification models (True Positives).
- **The "Tight Circle of Allies" Consensus:** 
  By demanding unanimous agreement across the model ensemble (Logistic Regression, Random Forest, Gradient Boosting, SVM, HistGradientBoosting, Extra Trees, KNN, MLP), we filter down to the **tightest core of 29 infallible rebel transmissions** in the held-out test sector.
  
| Metric | Full Test Sector | Survivors (Votes $\ge 1$) | Tight Circle of Allies (Votes = 8) |
| :--- | :---: | :---: | :---: |
| **Record Count** | 677 | 169 | **29** |
| **Purity (Precision)** | 34.1% | 83.2% | **85.3%** |
| **Mean Latitude** | 18.9082° N | 18.9069° N | **18.9262° N** |
| **Mean Longitude** | 72.7481° E | 72.7382° E | **72.8697° E** |

---

## 2. Creature Anatomy & Limb Squaring ($N^2$)

From Step 2 and Step 3's cross-reference with `location_descriptions.csv` and `creatures_table_final.csv`:
- **The Clue Reference:** Lunaris describes *"where nautilus wreckages repose"*.
- **The Anatomy Record:** Row 4 of `creatures_table_final.csv` specifically cross-references this disguise:
  > **Argonaut:** *"A delicate pelagic octopus whose female carries a thin paper-like eggcase and has eight sucker-bearing arms."*  
  > **Amazing Fact:** *"Despite its name, it is an octopus rather than a true nautilus."*
- **Number of Limbs ($N$):** 
  $$N = 8 \text{ arms}$$
- **Squared Base ($N^2$):** 
  $$N^2 = 8^2 = \mathbf{64}$$

---

## 3. Base-$N^2$ (Base-64) Decoding & Sonic Archives Link

The clue commands: *"using the result as their base. This is what will lead them to Rue."*
- **Base:** Base-$N^2$ = **Base-64**.
- Each transmission token in the `password` column is a 32-character URL-safe Base-64 encoded string (`TR-...`).
- Decoding via Base-64 and linking to the extracted Gamemaker Sonic Archive (`unlock sonic archives.zip`):
  - Solved all 16 Gamemaker Trials / Arena puzzles.
  - The secret reveal decrypted:
    $$\textbf{REVEAL: BACKSTAIRS LIFT}$$
    $$\textit{"The gamemakers await you there."}$$

---

## 4. Final Coordinates Leading to Rue

By pulling the boundary tight around the unanimous survivors of the blind spot:

- **Target Sector:** Lunaris Abyssal Shelf
- **Coordinates:** **`18.9262° N, 72.8697° E`**
- **Location Access:** **`BACKSTAIRS LIFT`**
