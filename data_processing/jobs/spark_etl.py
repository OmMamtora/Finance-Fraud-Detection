from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format, lower, to_timestamp, trim, when

from utils.logger import get_logger


logger = get_logger(__name__)


def run_spark_etl(input_path: str, output_path: str) -> None:
    input_uri = Path(input_path).resolve().as_uri()
    output_uri = Path(output_path).resolve().as_uri()

    spark = (
        SparkSession.builder.appName("fraud-detection-etl")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.hadoop.fs.defaultFS", "file:///")
        .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")
        .getOrCreate()
    )

    logger.info("Reading raw data from %s", input_uri)
    df = spark.read.csv(input_uri, header=True, inferSchema=True)

    cleaned_df = (
        df.dropDuplicates()
        .dropna(how="all")
        .withColumn("transaction_timestamp", to_timestamp(col("timestamp")))
        .withColumn("transaction_type", lower(trim(col("transaction_type"))))
        .withColumn("merchant_category", lower(trim(col("merchant_category"))))
        .withColumn("location", lower(trim(col("location"))))
        .withColumn("device_used", lower(trim(col("device_used"))))
        .withColumn("payment_channel", lower(trim(col("payment_channel"))))
        .withColumn("amount", when(col("amount").isNull(), 0).otherwise(col("amount")))
        .withColumn("transaction_date", date_format(col("transaction_timestamp"), "yyyy-MM-dd"))
    )

    logger.info("Writing processed data to %s", output_uri)
    cleaned_df.write.mode("overwrite").parquet(output_uri)
    spark.stop()


if __name__ == "__main__":
    run_spark_etl(
        input_path="Data/raw/financial_fraud_detection_dataset.csv",
        output_path="Data/processed/transactions_parquet",
    )
