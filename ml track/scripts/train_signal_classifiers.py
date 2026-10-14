"""
Signal Hardening and Model Comparison
Step 5: Train and compare multiple ML models to separate protected rebel signals from standard noise
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, average_precision_score, confusion_matrix,
    classification_report
)

# Models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

def main():
    print("=" * 80)
    print("STEP 5: HARDEN & CLASSIFY SIGNALS (MODEL COMPARISON)")
    print("=" * 80)
    
    # 1. Load data
    df = pd.read_csv('lunaris_with_density.csv')
    print(f"Loaded {len(df)} records from lunaris_with_density.csv")
    
    # Check cluster merge if available
    if os.path.exists('sonar_clustered_k8.csv'):
        try:
            k8 = pd.read_csv('sonar_clustered_k8.csv', usecols=['chest_id', 'cluster', 'dist_to_centroid'])
            df = df.merge(k8, on='chest_id', how='left')
            print("Successfully merged cluster and dist_to_centroid features.")
        except Exception as e:
            print("Cluster merge skipped:", e)
            
    # Target definition
    # protected = 1 (rebel signal), standard = 0 (background noise)
    df['target'] = (df['archive_class'].str.lower().str.strip() == 'protected').astype(int)
    pos_count = df['target'].sum()
    neg_count = len(df) - pos_count
    print(f"Target distribution: Protected (1) = {pos_count} ({pos_count/len(df)*100:.1f}%), Standard (0) = {neg_count} ({neg_count/len(df)*100:.1f}%)")
    
    # Define features
    num_features = [
        'longitude', 'latitude', 'sonar_depth', 'signal_quality', 
        'compass_bearing', 'soil_density', 'magnetic_reading', 'artefact_age', 
        'recovery_attempts', 'condition_score', 'recovery_distance_km', 
        'worth', 'weight_kg', 'treasure_density'
    ]
    if 'dist_to_centroid' in df.columns:
        num_features.append('dist_to_centroid')
        
    cat_features = ['material', 'seal_integrity', 'inspection_priority', 'sonar_operator', 'expedition_zone']
    if 'cluster' in df.columns:
        cat_features.append('cluster')
        
    # Filter features that exist
    num_features = [f for f in num_features if f in df.columns]
    cat_features = [f for f in cat_features if f in df.columns]
    
    print(f"Numerical features ({len(num_features)}): {num_features}")
    print(f"Categorical features ({len(cat_features)}): {cat_features}")
    
    X = df[num_features + cat_features].copy()
    y = df['target'].values
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"\nTrain set: {len(X_train)} samples ({y_train.sum()} protected, {len(y_train)-y_train.sum()} standard)")
    print(f"Test set:  {len(X_test)} samples ({y_test.sum()} protected, {len(y_test)-y_test.sum()} standard)")
    
    # Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
        ]
    )
    
    # Define classifiers to pit against each other
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=150, learning_rate=0.1, max_depth=4, random_state=42),
        "HistGradientBoosting": HistGradientBoostingClassifier(max_iter=150, random_state=42, class_weight='balanced'),
        "Support Vector Machine (RBF)": SVC(kernel='rbf', probability=True, class_weight='balanced', random_state=42),
        "Extra Trees": ExtraTreesClassifier(n_estimators=200, class_weight='balanced', random_state=42, n_jobs=-1),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=7),
        "Neural Network (MLP)": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
    }
    
    # Cross-validation comparison
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_results = []
    
    print("\n" + "=" * 80)
    print("5-FOLD STRATIFIED CROSS-VALIDATION PERFORMANCE")
    print("=" * 80)
    
    for name, clf in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])
        
        scoring = {
            'accuracy': 'accuracy',
            'balanced_accuracy': 'balanced_accuracy',
            'precision': 'precision',
            'recall': 'recall',
            'f1': 'f1',
            'roc_auc': 'roc_auc',
            'avg_precision': 'average_precision'
        }
        
        scores = cross_validate(pipeline, X_train, y_train, cv=cv, scoring=scoring, n_jobs=-1)
        
        cv_results.append({
            'Model': name,
            'CV_Accuracy': scores['test_accuracy'].mean(),
            'CV_Balanced_Acc': scores['test_balanced_accuracy'].mean(),
            'CV_Precision': scores['test_precision'].mean(),
            'CV_Recall (Protected)': scores['test_recall'].mean(),
            'CV_F1': scores['test_f1'].mean(),
            'CV_ROC_AUC': scores['test_roc_auc'].mean(),
            'CV_PR_AUC': scores['test_avg_precision'].mean()
        })
        print(f"Completed CV for {name:<28} | F1: {scores['test_f1'].mean():.4f} | Recall: {scores['test_recall'].mean():.4f} | ROC-AUC: {scores['test_roc_auc'].mean():.4f}")
        
    df_cv = pd.DataFrame(cv_results).sort_values(by='CV_F1', ascending=False)
    print("\nCross-Validation Summary Table:")
    print(df_cv.to_string(index=False))
    
    # Evaluate on held-out test set
    print("\n" + "=" * 80)
    print("HELD-OUT TEST SET EVALUATION (N = 677)")
    print("=" * 80)
    
    test_evaluations = []
    fitted_pipelines = {}
    
    for name, clf in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])
        pipeline.fit(X_train, y_train)
        fitted_pipelines[name] = pipeline
        
        y_pred = pipeline.predict(X_test)
        if hasattr(pipeline, "predict_proba"):
            y_proba = pipeline.predict_proba(X_test)[:, 1]
        else:
            y_proba = pipeline.decision_function(X_test)
            
        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()
        
        # Blind spot calculation: How many protected signals were misclassified as standard?
        # That is exactly FN (False Negatives: actual protected, predicted standard)
        fn_rate = fn / (tp + fn) if (tp + fn) > 0 else 0
        
        acc = accuracy_score(y_test, y_pred)
        bal_acc = balanced_accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_proba)
        pr_auc = average_precision_score(y_test, y_proba)
        
        test_evaluations.append({
            'Model': name,
            'Accuracy': acc,
            'Balanced_Acc': bal_acc,
            'Precision': prec,
            'Recall (Protected)': rec,
            'F1_Score': f1,
            'ROC_AUC': roc_auc,
            'PR_AUC': pr_auc,
            'TP (Protected Caught)': tp,
            'FN (Protected Missed)': fn,
            'FP (Standard Flagged)': fp,
            'TN (Standard Filtered)': tn,
            'Miss_Rate (Blind Spot)': fn_rate
        })
        
    df_test = pd.DataFrame(test_evaluations).sort_values(by='F1_Score', ascending=False)
    print("\nHeld-out Test Results (Sorted by F1-Score):")
    print(df_test[['Model', 'Accuracy', 'Balanced_Acc', 'Precision', 'Recall (Protected)', 'F1_Score', 'ROC_AUC', 'FN (Protected Missed)', 'Miss_Rate (Blind Spot)']].to_string(index=False))
    
    # Save CSV comparison
    df_test.to_csv('model_comparison_results.csv', index=False)
    df_cv.to_csv('model_cross_validation_results.csv', index=False)
    
    # Select best model
    best_model_name = df_test.iloc[0]['Model']
    best_pipeline = fitted_pipelines[best_model_name]
    print(f"\n>>> CHAMPION MODEL: {best_model_name} <<<")
    
    # Feature Importance for Champion / Tree Model
    print("\n" + "=" * 80)
    print(f"FEATURE IMPORTANCE ANALYSIS")
    print("=" * 80)
    
    # Check feature importance of Random Forest and Gradient Boosting
    for m_name in ['Random Forest', 'Gradient Boosting', 'Extra Trees']:
        if m_name in fitted_pipelines:
            m = fitted_pipelines[m_name]
            clf_step = m.named_steps['classifier']
            prep_step = m.named_steps['preprocessor']
            cat_encoder = prep_step.named_transformers_['cat']
            cat_encoded_cols = cat_encoder.get_feature_names_out(cat_features).tolist()
            all_feat_names = num_features + cat_encoded_cols
            
            importances = clf_step.feature_importances_
            feat_imp_df = pd.DataFrame({
                'Feature': all_feat_names,
                'Importance': importances
            }).sort_values(by='Importance', ascending=False)
            
            print(f"\nTop 15 Most Influential Features ({m_name}):")
            print(feat_imp_df.head(15).to_string(index=False))
            feat_imp_df.to_csv(f"feature_importance_{m_name.lower().replace(' ', '_')}.csv", index=False)
            
    # Generate test predictions and save
    test_preds_df = X_test.copy()
    test_preds_df['actual_archive_class'] = np.where(y_test == 1, 'protected', 'standard')
    for name, pipeline in fitted_pipelines.items():
        test_preds_df[f'pred_{name}'] = np.where(pipeline.predict(X_test) == 1, 'protected', 'standard')
    test_preds_df.to_csv('test_set_model_predictions.csv', index=False)
    
    print("\nSaved:")
    print("  - model_comparison_results.csv")
    print("  - model_cross_validation_results.csv")
    print("  - feature_importance_random_forest.csv")
    print("  - feature_importance_gradient_boosting.csv")
    print("  - test_set_model_predictions.csv")
    print("\nExecution complete.")

if __name__ == '__main__':
    main()
