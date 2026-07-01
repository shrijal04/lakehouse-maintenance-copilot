from pyspark.sql import SparkSession

from spark.config import JDBC_JAR, WAREHOUSE_PATH


class SparkManager:

    _spark = None

    def get_spark(self):

        if SparkManager._spark is None:

            SparkManager._spark = (
                SparkSession.builder
                .appName("Lakehouse Maintenance Copilot")
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

                # Enable Iceberg SQL
                .config(
                    "spark.sql.extensions",
                    "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
                )

                # Local Iceberg Catalog
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

            SparkManager._spark.sparkContext.setLogLevel(
                "WARN"
            )

        return SparkManager._spark

    def stop(self):

        if SparkManager._spark:

            SparkManager._spark.stop()

            SparkManager._spark = None