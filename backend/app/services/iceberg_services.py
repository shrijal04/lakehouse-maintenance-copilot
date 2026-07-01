from maintenance.health_metric import get_table_health
from spark.manager import get_spark

CATALOG = "local"
DATABASE = "lakehouse"


def get_all_tables():
    """
    Returns all Iceberg tables inside local.lakehouse.
    """

    spark = get_spark()

    tables = spark.sql(f"SHOW TABLES IN {CATALOG}.{DATABASE}")

    result = []

    for row in tables.collect():

        table_name = row.tableName

        # Skip demo tables
        if table_name.endswith("_demo"):
            continue

        full_table = f"{CATALOG}.{DATABASE}.{table_name}"

        try:
            health = get_table_health(spark, full_table)

            result.append(
                {
                    "table_name": table_name,
                    "full_name": full_table,
                    "health": health,
                }
            )

        except Exception as e:
            print(f"Skipping {table_name}: {e}")

    return result