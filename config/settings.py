from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    app_name: str = "Fraud Detection Platform"
    environment: str = "dev"
    aws_region: str = "ap-southeast-2"
    s3_bucket: str = "fraud-detection-data-lake11"
    model_path: str = str(BASE_DIR / "artifacts" / "models" / "final_stacking_model.joblib")
    processed_data_path: str = str(BASE_DIR / "data" / "processed" / "transactions_features.csv")
    log_dir: str = str(BASE_DIR / "logs")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
