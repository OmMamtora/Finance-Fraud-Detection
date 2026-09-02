import pandas as pd
import joblib
from pathlib import Path

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

# 📁 PATHS
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "processed" / "transactions_features.csv"
MODEL_DIR = BASE_DIR / "artifacts" / "models"

# 📊 LOAD DATA
df = pd.read_csv(DATA_PATH)

# 🎯 TARGET
target = "is_fraud"

X = df.drop(columns=[target])
y = df[target]

# 🔥 SAME TEST DATA FOR ALL MODELS
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 📦 MODEL FILES
models = {
    "Best Model": "best_model.joblib",
    "Final Model": "final_model.joblib",
    "Stacking Model": "stacking_model.joblib",
    "Mix Stacking": "mix_stacking_model.joblib"
}

results = []

# 🚀 LOOP THROUGH MODELS
for name, file in models.items():
    print(f"\n🔍 Evaluating {name}")

    model_path = MODEL_DIR / file

    if not model_path.exists():
        print(f"❌ Missing: {file}")
        continue

    model = joblib.load(model_path)

    # predictions
    y_pred = model.predict(X_test)

    try:
        y_prob = model.predict_proba(X_test)[:, 1]
    except:
        y_prob = y_pred  # fallback

    # metrics
    metrics = {
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1 Score": f1_score(y_test, y_pred),
        "ROC AUC": roc_auc_score(y_test, y_prob)
    }

    results.append(metrics)

# 📊 RESULTS TABLE
results_df = pd.DataFrame(results)

print("\n📊 MODEL COMPARISON:")
print(results_df.sort_values(by="ROC AUC", ascending=False))

# 💾 SAVE
results_df.to_csv(BASE_DIR / "artifacts" / "reports" / "model_comparison.csv", index=False)