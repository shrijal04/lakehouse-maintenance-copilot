import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from simulation.spark_factory import create_spark

TABLE = "local.silver.orders"


def main():

    spark = create_spark("OCC Session B")

    try:

        print("=" * 60)
        print("SESSION B")
        print("=" * 60)

        print("Updating immediately...")

        spark.sql(f"""
            UPDATE {TABLE}
            SET status='SESSION_B'
            WHERE order_id = 1
        """)

        print("SESSION B committed successfully.")

    finally:

        spark.stop()


if __name__ == "__main__":
    main()