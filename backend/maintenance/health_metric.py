import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "spark"))

from spark.session import create_spark_session

spark = create_spark_session()

TABLE = "local.lakehouse.orders"

print("=" * 60)
print("Lakehouse Health Report")
print("=" * 60)

# ---------------------------------------------------
# Snapshot Count
# ---------------------------------------------------

snapshot_count = spark.sql(f"""
SELECT COUNT(*) AS snapshots
FROM {TABLE}.snapshots
""").collect()[0]["snapshots"]

# ---------------------------------------------------
# Data File Metrics
# ---------------------------------------------------

files = spark.sql(f"""
SELECT
    COUNT(*) AS file_count,
    ROUND(AVG(file_size_in_bytes) / 1024, 2) AS avg_file_kb,
    ROUND(SUM(file_size_in_bytes) / 1024 / 1024, 2) AS total_size_mb
FROM {TABLE}.files
""").collect()[0]

# ---------------------------------------------------
# Print Report
# ---------------------------------------------------

print(f"Table           : {TABLE}")
print(f"Snapshots       : {snapshot_count}")
print(f"Data Files      : {files['file_count']}")
print(f"Average File KB : {files['avg_file_kb']}")
print(f"Total Size MB   : {files['total_size_mb']}")

spark.stop()