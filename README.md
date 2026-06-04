# 🛡️ Smart FinGuard – AI-Powered Financial Fraud Detection Platform

## 📌 Overview

Smart FinGuard is an end-to-end Financial Fraud Detection Platform that combines Machine Learning, Big Data Processing, Cloud Technologies, Workflow Automation, and Real-Time Risk Intelligence to identify suspicious financial transactions.

The platform processes millions of transaction records, engineers fraud-specific behavioral features, trains predictive models, and serves real-time fraud predictions through a FastAPI-powered backend and interactive web dashboard.

This project demonstrates a complete industry-style Data Science and AI Engineering workflow, covering data ingestion, feature engineering, model development, deployment, monitoring, and cloud integration.

---

## 🚀 Key Highlights

✅ End-to-End Fraud Detection Pipeline

✅ Apache Spark Big Data Processing

✅ AWS S3 Cloud Storage Integration

✅ Apache Airflow Workflow Automation

✅ Advanced Machine Learning Models

✅ Stacking Ensemble Architecture

✅ FastAPI Deployment

✅ Interactive Fraud Detection Dashboard

✅ Real-Time Transaction Risk Scoring

✅ Cloud-Ready Scalable Architecture

✅ Deep Learning Research & Development

---

# 🎯 Problem Statement

Financial institutions process millions of transactions every day, making manual fraud detection impossible.

Traditional rule-based systems often fail to detect evolving fraud patterns and sophisticated attacks.

Smart FinGuard addresses these challenges by building an intelligent fraud detection platform capable of:

* Processing large-scale transaction datasets
* Detecting abnormal behavioral patterns
* Identifying fraudulent transactions
* Supporting real-time decision-making
* Providing scalable fraud intelligence

---

# 🏗️ System Architecture

```text
Raw Transaction Data
        │
        ▼
AWS S3 Storage
        │
        ▼
Data Ingestion Pipeline
        │
        ▼
Apache Spark ETL Processing
        │
        ▼
Feature Engineering
        │
        ▼
EDA & Analytics
        │
        ▼
Machine Learning Pipeline
        │
        ▼
Model Evaluation
        │
        ▼
FastAPI Inference Service
        │
        ▼
Web Dashboard
        │
        ▼
Fraud Risk Intelligence
```

---

# 📂 Project Structure

```bash
Finance-Fraud-Detection/
│
├── airflow_dags/
├── api_service/
├── artifacts/
├── config/
│
├── Data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── data_ingestion/
├── data_processing/
├── eda/
├── feature_engineering/
├── model_training/
├── model_evaluation/
│
├── docs/
├── logs/
├── tests/
├── utils/
│
├── web_app/
│   ├── templates/
│   └── static/
│
├── requirements.txt
├── README.md
└── FileManagement.txt
```

---

# 📊 Dataset Availability

> ⚠️ Dataset Not Included in Repository

The dataset used in this project is not included in the GitHub repository due to its large size (5M+ transaction records).

### Dataset Download

Google Drive:

```text
https://drive.google.com/file/d/1OzhnR8K3X029BEFfaim8SlTK4PsUuQ6R/view?usp=drive_link
```

### Dataset Placement

```bash
Data/
├── raw/
├── processed/
└── external/
```

### Why Is The Dataset External?

* Dataset size exceeds GitHub storage recommendations
* Contains millions of financial transaction records
* Improves repository performance and cloning speed
* Standard industry practice for Data Science projects

---

# 📈 Dataset Statistics

| Metric              | Value      |
| ------------------- | ---------- |
| Total Transactions  | 5,000,000+ |
| Fraud Cases         | 179,553+   |
| Fraud Ratio         | 3.59%      |
| Original Features   | 18         |
| Engineered Features | 27         |

---

# 🔧 Feature Engineering

The platform generates advanced fraud-specific features including:

* Transaction Hour
* Transaction Day of Week
* Customer Average Spending
* Spending Deviation Score
* Merchant Frequency
* Transaction Velocity
* Geo Anomaly Score
* Time Since Last Transaction
* Night Transaction Flag
* Behavioral Risk Indicators

These engineered features improve fraud detection capability and anomaly identification.

---

# 🤖 AI Models

## Traditional Machine Learning Models

* Logistic Regression
* Random Forest
* XGBoost
* LightGBM
* Stacking Ensemble

### Final Ensemble Architecture

**Base Models**

* Random Forest
* XGBoost
* LightGBM

**Meta Learner**

* Logistic Regression

The stacking architecture combines multiple algorithms to improve prediction performance and robustness.

---

## Deep Learning (Currently Under Development)

The project is actively being enhanced with Deep Learning techniques for improved fraud detection performance.

Research Areas:

* Artificial Neural Networks (ANN)
* Autoencoders for Anomaly Detection
* Deep Learning Ensembles
* Hybrid ML + DL Architectures
* Advanced Imbalanced Learning Strategies

---

# 📊 Model Evaluation

The system evaluates models using:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* Confusion Matrix

Generated Reports:

* ROC Curves
* Precision-Recall Curves
* Correlation Heatmaps
* Target Distribution Analysis
* Feature Importance Analysis
* Prediction Probability Distribution

---

# ⚙️ Installation

## Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

```bash
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks execution:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure AWS

```bash
aws configure
```

Provide:

```text
Access Key
Secret Key
Region: eu-north-1
Output: json
```

---

# 🚀 Running the Pipeline

### Upload Raw Data to AWS S3

```bash
python -m data_ingestion.scripts.local_to_s3
```

### Run Feature Engineering

```bash
python -m feature_engineering.pipelines.build_features
```

### Run Exploratory Data Analysis

```bash
python -m eda.analyze
```

### Train Models

```bash
python -m model_training.trainers.train_models
```

### Evaluate Models

```bash
python -m model_evaluation.evaluate
```

---

# 🌐 Run FastAPI Backend

```bash
uvicorn api_service.app.main:app --reload
```

Available Endpoints:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

---

# 🖥️ Run Dashboard

```bash
uvicorn web_app.app:app --reload --port 8502
```

Dashboard URL:

```text
http://127.0.0.1:8502/
```

---

# 🔄 Workflow Automation

Apache Airflow manages:

* Data Ingestion
* ETL Processing
* Feature Engineering
* Model Retraining
* Pipeline Monitoring

---

# ☁️ Technology Stack

### Programming

* Python

### Machine Learning

* Scikit-Learn
* XGBoost
* LightGBM

### Deep Learning

* TensorFlow (In Progress)
* PyTorch (Research Phase)

### Big Data

* Apache Spark
* PySpark

### Workflow Automation

* Apache Airflow

### Cloud

* AWS S3

### Backend

* FastAPI

### Frontend

* HTML
* CSS
* Jinja2

### Visualization

* Matplotlib
* Seaborn

---

# 🚧 Current Development Status

Smart FinGuard is actively under development. The current version includes a complete Machine Learning pipeline, Big Data processing workflow, cloud integration, and deployment infrastructure.

Future development focuses on integrating Deep Learning models and advanced anomaly detection techniques to further improve fraud detection performance.

---

# 👨‍💻 Team

### Smart FinGuard Development Team

* Om Mamtora
* Riya Dhorajiya
* Hemangi Vaghasiya
* Varun Kumbhani
* Mitali Rafaliya

### Academic Program

**Master of Science in Data Science**

**Symbiosis Skills and Professional University**

---

# 📜 License

This project is developed for academic, educational, and research purposes.
