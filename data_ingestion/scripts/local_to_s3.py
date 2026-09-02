from pathlib import Path

from utils.logger import get_logger
from utils.s3 import S3Client


logger = get_logger(__name__)


def upload_local_dataset_to_s3(local_file: str, s3_key: str) -> None:
    """
    Upload the locally available raw fraud dataset into S3.
    """
    dataset = Path(local_file)
    if not dataset.exists():
        raise FileNotFoundError(f"Dataset not found: {local_file}")

    s3_client = S3Client()
    s3_client.upload_file(str(dataset), s3_key)
    logger.info("Raw dataset uploaded successfully.")


if __name__ == "__main__":
    upload_local_dataset_to_s3(
        local_file="Data/raw/financial_fraud_detection_dataset.csv",
        s3_key="raw/transactions/financial_fraud_detection_dataset.csv",
    )
