import os
import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    classification_report, recall_score, roc_auc_score,
    precision_score, f1_score, confusion_matrix,
    precision_recall_curve, roc_curve, accuracy_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import StackingClassifier

from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

sns.set(style="whitegrid")

import warnings
warnings.filterwarnings("ignore")
# ==============================
# PLOT FUNCTION (YOUR CODE)
# ==============================
def save_all_plots(
    y_train, y_test, proba, cm,
    precision_arr, recall_arr, thresholds,
    roc_auc, X_train, num_cols,
    output_dir="artifacts/plots"
):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(6,4))
    sns.countplot(x=y_train)
    plt.title("Target Distribution")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/target_distribution.png", dpi=300)
    plt.close()

    cols_to_plot = num_cols[:10] if len(num_cols) > 10 else num_cols
    X_train[cols_to_plot].hist(figsize=(15,10), bins=30)
    plt.suptitle("Numerical Feature Distribution")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/numerical_distribution.png", dpi=300)
    plt.close()

    sample_data = X_train[num_cols]
    if len(sample_data) > 5000:
        sample_data = sample_data.sample(5000, random_state=42)

    plt.figure(figsize=(12,8))
    sns.heatmap(sample_data.corr(), cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/correlation_heatmap.png", dpi=300)
    plt.close()

    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/confusion_matrix.png", dpi=300)
    plt.close()

    fpr, tpr, _ = roc_curve(y_test, proba)
    plt.figure(figsize=(6,5))
    plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.4f}")
    plt.plot([0,1], [0,1], linestyle='--')
    plt.legend()
    plt.title("ROC Curve")
    plt.savefig(f"{output_dir}/roc_curve.png", dpi=300)
    plt.close()

    plt.figure(figsize=(6,5))
    plt.plot(recall_arr, precision_arr)
    plt.title("Precision-Recall Curve")
    plt.savefig(f"{output_dir}/precision_recall_curve.png", dpi=300)
    plt.close()

    f1_scores = 2 * (precision_arr * recall_arr) / (precision_arr + recall_arr + 1e-10)
    plt.figure(figsize=(6,5))
    plt.plot(thresholds, f1_scores[:-1])
    plt.title("Threshold vs F1 Score")
    plt.savefig(f"{output_dir}/threshold_vs_f1.png", dpi=300)
    plt.close()

    plt.figure(figsize=(6,4))
    sns.histplot(proba, bins=50)
    plt.title("Prediction Probability Distribution")
    plt.savefig(f"{output_dir}/prediction_distribution.png", dpi=300)
    plt.close()

    print(f"\n📁 All plots saved at: {output_dir}")


# ==============================
# TRAIN FUNCTION
# ==============================
def train_models(data_path, target_column, model_output_dir="artifacts/models"):

    print("\n🚀 STAGE 1: Loading Data")
    df = pd.read_csv(data_path)

    SAMPLE_SIZE = 1500000

    if len(df) > SAMPLE_SIZE:

        print(f"\n📦 Using Sample Dataset: {SAMPLE_SIZE}")

        df = df.sample(
            n=SAMPLE_SIZE,
            random_state=42
        )

    print("Sample Shape:", df.shape)
    # ==============================
    # DROP COLUMNS
    # ==============================
    print("\n🧹 STAGE 2: Cleaning Data")

    # drop_cols = [
    #     "transaction_id", "ip_address", "device_hash",
    #     "fraud_type", "timestamp"
    # ]

    df = df.drop(columns=["transaction_id", "ip_address", "device_hash", "fraud_type", "timestamp"])

    # Feature engineering
    df["amount_ratio"] = df["amount"] / (df["customer_avg_amount"] + 1)

    print("Shape:", df.shape)
    print("Fraud Ratio:\n", df[target_column].value_counts(normalize=True))

    # ==============================
    # SPLIT
    # ==============================
    print("\n✂️ STAGE 3: Train-Test Split")

    X = df.drop(columns=[target_column])
    y = df[target_column].astype(int)

    bool_cols = X.select_dtypes(include=["bool"]).columns
    X[bool_cols] = X[bool_cols].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # ==============================
    # FEATURE TYPES
    # ==============================
    print("\n🧠 STAGE 4: Feature Engineering")

    num_cols = X_train.select_dtypes(include=["int64", "float64"]).columns
    cat_cols = X_train.select_dtypes(include=["object", "category", "string"]).columns

    # ==============================
    # PREPROCESSOR
    # ==============================
    print("\n⚙️ STAGE 5: Building Preprocessor")

    preprocessor = ColumnTransformer([
        ("num", SimpleImputer(strategy="median"), num_cols),

        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", min_frequency=0.01))
        ]), cat_cols)
    ])

    # ==============================
    # MODELS
    # ==============================
    

    print("\n🤖 STAGE 6: Initializing Stacking Model")

    rf = RandomForestClassifier(
        n_estimators=150,
        max_depth=10,
        # class_weight="balanced",
        class_weight={0:1, 1:3},
        random_state=42,
        n_jobs=-1
    )

    # scale_pos_weight = min((len(y_train) / sum(y_train)) - 1, 10)

    scale_pos_weight = 2

    xgb = XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_pos_weight,
        eval_metric="logloss",
        tree_method="hist",
        random_state=42
    )

    lgbm = LGBMClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=8,
        num_leaves=64,
        subsample=0.8,
        colsample_bytree=0.8,
        # class_weight="balanced"
        class_weight={0:1, 1:3},
        random_state=42,
        verbosity=-1
    )

    stack_model = StackingClassifier(

    estimators=[

        ('rf', rf),

        ('xgb', xgb),

        ('lgbm', lgbm)
    ],

        final_estimator=LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    ),

    passthrough=True,

    n_jobs=-1
)
    Path(model_output_dir).mkdir(parents=True, exist_ok=True)

    # ==============================
    # TRAIN LOOP
    # ==============================
    print("\n🔥 STAGE 7: Training Stacking Model")

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", stack_model)
    ])

    pipeline.fit(X_train, y_train)

    # ==============================
    # PREDICTION
    # ==============================
    proba = pipeline.predict_proba(X_test)[:, 1]

    # ==============================
    # THRESHOLD TUNING
    # ==============================
    print("\n🎯 STAGE 8: Threshold Tuning")

    precision_arr, recall_arr, thresholds = precision_recall_curve(y_test, proba)

    f1_scores = 2 * (precision_arr * recall_arr) / (precision_arr + recall_arr + 1e-10)
    best_idx = np.argmax(f1_scores)

    # threshold = thresholds[best_idx]
    threshold = 0.6
    preds = (proba >= threshold).astype(int)
  
    # ==============================
    # METRICS
    # ==============================
    print("\n📊 STAGE 9: Evaluation")

    cm = confusion_matrix(y_test, preds)

    metrics = {
        "model": "stacking_model",
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds),
        "recall": recall_score(y_test, preds),
        "f1": f1_score(y_test, preds),
        "roc_auc": roc_auc_score(y_test, proba),
        "threshold": float(threshold),
        "confusion_matrix": cm.tolist()
    }

    print(json.dumps(metrics, indent=4))

    # ==============================
    # SAVE MODEL
    # ==============================
    print("\n💾 STAGE 10: Saving Model")

    import joblib
    joblib.dump(pipeline, Path(model_output_dir) / "final_stacking_model.joblib")

    # ==============================
    # SAVE REPORT
    # ==============================
    print("\n📝 STAGE 11: Saving Report")

    os.makedirs("artifacts/reports", exist_ok=True)

    with open("artifacts/reports/model_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    # ==============================
    # PLOTS
    # ==============================
    print("\n📈 STAGE 12: Generating Plots")

    save_all_plots(
        y_train, y_test, proba, cm,
        precision_arr, recall_arr, thresholds,
        metrics["roc_auc"], X_train, num_cols
    )

    print("\n✅ TRAINING COMPLETE")

    return metrics

if __name__ == "__main__":
    result = train_models(
        data_path="Data/processed/transactions_features.csv",
        target_column="is_fraud"
    )

    print("\n🎉 FINAL RESULT:", result)