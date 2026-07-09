import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from spark.manager import SparkManager

TABLE = "local.silver.orders"


def main():
    spark = SparkManager().get_spark()

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


if __name__ == "__main__":
    main()