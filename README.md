# 🛡️ Smart FinGuard – AI-Powered Financial Fraud Detection Platform

## 📌 Overview

Smart FinGuard is an end-to-end Financial Fraud Detection Platform that combines **Machine Learning, Big Data Processing, Cloud Technologies, Workflow Automation, and Risk Intelligence** to identify suspicious financial transactions.

The platform is designed to process millions of transaction records, engineer fraud-specific behavioral features, train predictive models, and serve fraud predictions through a **FastAPI backend and interactive dashboard**.

This project demonstrates an industry-style Data Science and AI Engineering workflow covering data ingestion, Spark processing, feature engineering, exploratory analysis, model development, evaluation, deployment infrastructure, workflow orchestration, and cloud integration.

---

## 🚀 Key Highlights

- ✅ End-to-End Fraud Detection Pipeline
- ✅ Apache Spark / PySpark Big Data Processing
- ✅ AWS S3 Cloud Storage Integration
- ✅ Apache Airflow Workflow Automation
- ✅ Advanced Machine Learning Models
- ✅ Stacking Ensemble Architecture
- ✅ FastAPI Prediction Service
- ✅ Interactive Fraud Detection Dashboard
- ✅ Transaction Risk Scoring
- ✅ Cloud-Ready Scalable Architecture
- 🚧 Deep Learning Research & Development

---

## 🎯 Problem Statement

Financial institutions process millions of transactions every day, making manual fraud detection impractical.

Traditional rule-based systems can struggle with evolving fraud patterns and sophisticated attacks. Smart FinGuard addresses this challenge by building an intelligent fraud detection platform capable of:

- Processing large-scale transaction datasets
- Detecting abnormal behavioral patterns
- Identifying potentially fraudulent transactions
- Supporting automated decision-making
- Providing scalable fraud intelligence

---

## 🏗️ System Architecture

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

## 📂 Project Structure

```text
Finance-Fraud-Detection/
│
├── airflow_dags/              # Airflow DAG workflows
├── api_service/               # FastAPI backend services
├── artifacts/                 # Models, plots and evaluation outputs
├── config/                    # Application configuration
│
├── Data/
│   ├── raw/                   # Local raw dataset (not committed)
│   ├── processed/             # Processed datasets (not committed)
│   └── external/              # External datasets
│
├── data_ingestion/            # Data ingestion modules
├── data_processing/           # Spark ETL processing
├── eda/                       # Exploratory Data Analysis
├── feature_engineering/       # Fraud feature generation
├── model_training/            # Model training
├── model_evaluation/          # Model evaluation
│
├── docs/                      # Project documentation
├── tests/                     # Automated tests
├── utils/                     # Reusable utilities
│
├── web_app/                   # Web application
│   ├── templates/
│   └── static/
│
├── requirements.txt
├── README.md
└── SmartFinGuard_Presentation.pptx
```

---

## 📊 Dataset

> ⚠️ **The large transaction datasets are not included in this GitHub repository.**

The dataset contains **5M+ transaction records** and is intentionally kept outside GitHub because of its large size.

### Dataset Download

The project dataset is available through Google Drive:

```text
https://drive.google.com/drive/folders/1BkwFHo_ng2IMF3AlMN7WAIdgCHGNg1mq?usp=drive_link
```

### Dataset Placement

After downloading the dataset, place it locally as:

```text
Data/
├── raw/
│   └── financial_fraud_detection_dataset.csv
├── processed/
└── external/
```

The raw and processed CSV files are excluded from the Git repository.

### Why Is The Dataset External?

- Dataset size is too large for standard GitHub repository storage
- Contains millions of transaction records
- Keeps repository cloning and downloads lightweight
- Follows a common practice for large-scale Data Science projects

---

## 📈 Dataset Statistics

| Metric | Value |
|---|---:|
| Total Transactions | 5,000,000+ |
| Fraud Cases | 179,553+ |
| Fraud Ratio | 3.59% |
| Original Features | 18 |
| Engineered Features | 27 |

---

## 🔧 Feature Engineering

The platform generates fraud-specific behavioral features including:

- Transaction Hour
- Transaction Day of Week
- Customer Average Spending
- Spending Deviation Score
- Merchant Frequency
- Transaction Velocity
- Geo Anomaly Score
- Time Since Last Transaction
- Night Transaction Flag
- Behavioral Risk Indicators

These features are designed to capture transaction behavior, spending anomalies, velocity patterns, and other signals useful for fraud detection.

---

## 🤖 Machine Learning Models

### Traditional Machine Learning

The project includes:

- Logistic Regression
- Random Forest
- XGBoost
- LightGBM
- Stacking Ensemble

### Final Stacking Architecture

**Base Models**

```text
Random Forest
XGBoost
LightGBM
```

**Meta Learner**

```text
Logistic Regression
```

The stacking architecture combines multiple models to improve prediction robustness.

### 🚧 Deep Learning

Deep Learning experimentation is currently under development and is planned as a future enhancement to the fraud detection pipeline.

---

## 📊 Model Evaluation

The system evaluates models using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix

Generated visualizations include:

- Target Distribution
- Correlation Heatmap
- Confusion Matrix
- ROC Curve
- Precision-Recall Curve
- Threshold vs F1 Score
- Prediction Probability Distribution

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/OmMamtora/Finance-Fraud-Detection.git
cd Finance-Fraud-Detection
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ☁️ AWS Configuration

Configure AWS CLI:

```bash
aws configure
```

Provide your own credentials securely.

Example:

```text
Access Key: YOUR_ACCESS_KEY
Secret Key: YOUR_SECRET_KEY
Region: eu-north-1
Output: json
```

> ⚠️ Never commit AWS credentials, API keys, passwords, or `.env` files to GitHub.

---

## 🚀 Running the Pipeline

### 1. Upload Raw Data to AWS S3

```bash
python -m data_ingestion.scripts.local_to_s3
```

### 2. Run Feature Engineering

```bash
python -m feature_engineering.pipelines.build_features
```

### 3. Run Exploratory Data Analysis

```bash
python -m eda.analyze
```

### 4. Train Models

```bash
python -m model_training.trainers.train_models
```

### 5. Evaluate Models

```bash
python -m model_evaluation.evaluate
```

---

## 🌐 Run FastAPI Backend

Start the API:

```bash
uvicorn api_service.app.main:app --reload
```

Available endpoints:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

The `/docs` endpoint provides the interactive FastAPI Swagger documentation.

---

## 🖥️ Run Web Dashboard

Start the web application:

```bash
uvicorn web_app.app:app --reload --port 8502
```

Open:

```text
http://127.0.0.1:8502/
```

---

## 🔄 Workflow Automation

Apache Airflow is used to orchestrate the machine learning workflow, including:

- Data ingestion
- ETL processing
- Feature engineering
- Model training / retraining
- Pipeline monitoring

---

## 🧪 Testing

The project contains tests for API and feature-related functionality.

Run:

```bash
pytest
```

---

## 🛠️ Technology Stack

### Programming

- Python

### Machine Learning

- Scikit-learn
- XGBoost
- LightGBM

### Big Data

- Apache Spark
- PySpark

### Workflow Automation

- Apache Airflow

### Cloud

- AWS S3

### Backend

- FastAPI
- Uvicorn

### Frontend / Web

- HTML
- CSS
- Jinja2

### Visualization & Analytics

- Power BI
- Matplotlib
- Seaborn

---

## 🚧 Current Development Status

Smart FinGuard is actively under development. The current version includes a complete Machine Learning pipeline, Big Data processing workflow, cloud integration, and deployment infrastructure.

Future development focuses on integrating Deep Learning models and advanced anomaly detection techniques to further improve fraud detection performance.

---

## 👨‍💻 Author

**Om Mamtora**

MSc Data Science | AI & Machine Learning Enthusiast

GitHub: https://github.com/OmMamtora

---

## ⭐ If You Find This Project Useful

Consider giving the repository a ⭐ on GitHub.
