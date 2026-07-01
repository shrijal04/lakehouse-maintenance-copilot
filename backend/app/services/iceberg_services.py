from maintenance.health_metric import HealthService
from spark.manager import SparkManager


class IcebergService:

    CATALOG = "local"
    DATABASE = "lakehouse"

    def __init__(self):

        self.spark = SparkManager().get_spark()
        self.health = HealthService(self.spark)

    def get_all_tables(self):
        """
        Returns all Iceberg tables inside local.lakehouse.
        """

        tables = self.spark.sql(
            f"SHOW TABLES IN {self.CATALOG}.{self.DATABASE}"
        )

        result = []

        for row in tables.collect():

            table_name = row.tableName

            # Skip demo tables
            if table_name.endswith("_demo"):
                continue

            full_table = (
                f"{self.CATALOG}."
                f"{self.DATABASE}."
                f"{table_name}"
            )

            try:

                health = self.health.get_table_health(
                    full_table
                )

                result.append(
                    {
                        "table_name": table_name,
                        "full_name": full_table,
                        "health": health,
                    }
                )

            except Exception as e:

                print(
                    f"Skipping {table_name}: {e}"
                )

        return result