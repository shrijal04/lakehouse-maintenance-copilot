from pyspark.sql import SparkSession

from spark.config import (
    JDBC_JAR,
    WAREHOUSE_PATH,
)


def create_spark(app_name: str):
    """
    Creates a brand-new SparkSession.

    Unlike SparkManager, this does NOT use
    the singleton pattern.

    Each call creates an independent session,
    allowing us to simulate concurrent users.
    """

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")

        # PostgreSQL JDBC
        .config(
            "spark.jars",
            JDBC_JAR,
        )

        # Iceberg Runtime
        .config(
            "spark.jars.packages",
            "org.apache.iceberg:iceberg-spark-runtime-4.1_2.13:1.11.0",
        )

        # Iceberg Extensions
        .config(
            "spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
        )

        # Local Catalog
        .config(
            "spark.sql.catalog.local",
            "org.apache.iceberg.spark.SparkCatalog",
        )

        .config(
            "spark.sql.catalog.local.type",
            "hadoop",
        )

        .config(
            "spark.sql.catalog.local.warehouse",
            WAREHOUSE_PATH,
        )

        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    return spark