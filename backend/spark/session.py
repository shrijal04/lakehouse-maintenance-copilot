from pyspark.sql import SparkSession
from config import JDBC_JAR, WAREHOUSE_PATH


def create_spark_session():

    spark = (
        SparkSession.builder
        .appName("Lakehouse Maintenance Copilot")
        .master("local[*]")

        # PostgreSQL JDBC
        .config("spark.jars", JDBC_JAR)

        # Automatically download Iceberg
        .config(
            "spark.jars.packages",
            "org.apache.iceberg:iceberg-spark-runtime-4.1_2.13:1.11.0"
        )

        # Enable Iceberg SQL
        .config(
            "spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
        )

        # Local catalog
        .config(
            "spark.sql.catalog.local",
            "org.apache.iceberg.spark.SparkCatalog"
        )

        .config(
            "spark.sql.catalog.local.type",
            "hadoop"
        )

        .config(
            "spark.sql.catalog.local.warehouse",
            WAREHOUSE_PATH
        )

        .getOrCreate()
        
    )

    spark.sparkContext.setLogLevel("WARN")

    return spark
