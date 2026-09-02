import json
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Fraud Dashboard", layout="wide")
st.title("Fraud Detection Dashboard")

data_path = Path("data/processed/transactions_features.csv")
metrics_path = Path("artifacts/reports/model_metrics.json")

if data_path.exists():
    df = pd.read_csv(data_path)
    st.metric("Total Transactions", len(df))
    if "is_fraud" in df.columns:
        st.metric("Fraud Ratio", f"{df['is_fraud'].mean():.2%}")
        st.bar_chart(df["is_fraud"].value_counts())
    if "amount" in df.columns:
        st.subheader("Transaction Amount Distribution")
        st.line_chart(df["amount"].head(200))
else:
    st.warning("Processed feature dataset not found.")

if metrics_path.exists():
    st.subheader("Model Metrics")
    with open(metrics_path, "r", encoding="utf-8") as file:
        metrics = json.load(file)
    st.json(metrics)

