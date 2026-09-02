from pathlib import Path

import boto3

from config.settings import settings
from utils.logger import get_logger


logger = get_logger(__name__)


class S3Client:
    def __init__(self, bucket_name: str | None = None, region_name: str | None = None) -> None:
        self.bucket_name = bucket_name or settings.s3_bucket
        self.client = boto3.client("s3", region_name=region_name or settings.aws_region)

    def upload_file(self, local_path: str, s3_key: str) -> None:
        logger.info("Uploading %s to s3://%s/%s", local_path, self.bucket_name, s3_key)
        self.client.upload_file(local_path, self.bucket_name, s3_key)

    def download_file(self, s3_key: str, local_path: str) -> None:
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)
        logger.info("Downloading s3://%s/%s to %s", self.bucket_name, s3_key, local_path)
        self.client.download_file(self.bucket_name, s3_key, local_path)

