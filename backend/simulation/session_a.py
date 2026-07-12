import sys
import os
import time

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from pyspark.errors.exceptions.captured import Py4JJavaError
from simulation.spark_factory import create_spark

TABLE = "local.silver.orders"


def main():

    spark = create_spark("OCC Session A")

    try:

        print("=" * 60)
        print("SESSION A")
        print("=" * 60)

        print("Reading table...")

        spark.sql(f"""
            SELECT *
            FROM {TABLE}
            LIMIT 5
        """).show()

        print()
        print("Snapshot loaded successfully.")
        print()
        print("Sleeping for 20 seconds...")

        time.sleep(20)

        print()
        print("Trying UPDATE...")

        spark.sql(f"""
            UPDATE {TABLE}
            SET status='SESSION_A'
            WHERE order_id = 1
        """)

        print()
        print("SESSION A committed successfully.")

        sys.exit(0)

    except Py4JJavaError as e:

        message = str(e)

        if (
            "ValidationException" in message
            or "Found conflicting files" in message
        ):

            print()
            print("############################################")
            print("OPTIMISTIC CONCURRENCY CONFLICT DETECTED")
            print("Another session committed changes first.")
            print("Iceberg rejected this transaction.")
            print("############################################")

            sys.exit(1)

        else:

            print()
            print("Unexpected Spark Error")
            print(message)

            sys.exit(1)

    except Exception as e:

        print()
        print("Unexpected Error")
        print(str(e))

        sys.exit(1)

    finally:

        spark.stop()


if __name__ == "__main__":
    main()