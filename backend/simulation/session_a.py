import sys
import os
import time

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from spark.manager import SparkManager

spark = SparkManager().get_spark()

TABLE = "local.lakehouse.orders"

print("=" * 60)
print("SESSION A")
print("=" * 60)

print("Reading table...")

spark.sql(f"""
SELECT *
FROM {TABLE}
LIMIT 5
""").show()

print("\nSleeping for 20 seconds...")
print("Run session_b.py NOW.\n")

time.sleep(20)

print("Trying UPDATE...")

spark.sql(f"""
UPDATE {TABLE}
SET status='SESSION_A'
WHERE order_id = 1
""")

print("\nSESSION A committed successfully.")