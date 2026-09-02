import json
from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
    roc_curve,
    accuracy_score
)

from utils.common import load_model


def evaluate_model(
    model_path: str,
    data_path: str,
    target_column: str,
    output_path: str,
    threshold: float = 0.5,
    feature_path: str = None,
    anomaly_model_path: str = None
) -> dict:

    # =========================
    # LOAD MODEL & DATA
    # =========================
    model = load_model(model_path)
    df = pd.read_csv(data_path)

    drop_if_present = ["transaction_id", "ip_address", "device_hash", "fraud_type", "timestamp"]
    df = df.drop(columns=[col for col in drop_if_present if col in df.columns])

    X = df.drop(columns=[target_column])
    y = df[target_column].astype(int)

    # =========================
    # TYPE FIXES
    # =========================
    bool_cols = X.select_dtypes(include=["bool"]).columns
    X[bool_cols] = X[bool_cols].astype(int)

    # =========================
    # ADD ANOMALY SCORE
    # =========================
    if "anomaly_score" not in X.columns:
        if anomaly_model_path and Path(anomaly_model_path).exists():
            print("✅ Generating anomaly_score using saved model")
            anomaly_model = load_model(anomaly_model_path)
            X["anomaly_score"] = anomaly_model.predict(X)
        else:
            print("⚠️ anomaly_score missing → using default 0")
            X["anomaly_score"] = 0

    # =========================
    # FEATURE ALIGNMENT (SAFE)
    # =========================
    if feature_path and Path(feature_path).exists():
        print("✅ Applying feature alignment")
        expected_cols = load_model(feature_path)

        # Add missing columns
        for col in expected_cols:
            if col not in X.columns:
                X[col] = 0

        # Remove extra columns
        X = X[expected_cols]

    else:
        print("⚠️ feature_columns not found → skipping alignment")

    # =========================
    # PREDICTIONS
    # =========================
    proba = model.predict_proba(X)[:, 1]
    preds = (proba >= threshold).astype(int)

    # =========================
    # METRICS
    # =========================
    precision = precision_score(y, preds, zero_division=0)
    recall = recall_score(y, preds, zero_division=0)
    f1 = f1_score(y, preds, zero_division=0)
    accuracy = accuracy_score(y, preds)
    roc_auc = roc_auc_score(y, proba)

    cm = confusion_matrix(y, preds)
    cm_normalized = (cm.astype(float) / cm.sum(axis=1, keepdims=True)).tolist()

    fpr, tpr, _ = roc_curve(y, proba)

    # =========================
    # SAVE RESULTS
    # =========================
    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": roc_auc,
        "threshold": threshold,
        "confusion_matrix": cm.tolist(),
        "confusion_matrix_normalized": cm_normalized,
        "classification_report": classification_report(y, preds, output_dict=True),
        "roc_curve": {
            "fpr": fpr.tolist(),
            "tpr": tpr.tolist()
        }
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("✅ Evaluation complete. Metrics saved.")

    return metrics


if __name__ == "__main__":
    evaluate_model(
        model_path="artifacts/models/stacking_model.joblib",
        data_path="Data/processed/transactions_features.csv",
        target_column="is_fraud",
        output_path="artifacts/reports/model_metrics.json",
        threshold=0.4,
        feature_path="artifacts/features/feature_columns.joblib",  # safe now
        anomaly_model_path=None
    )