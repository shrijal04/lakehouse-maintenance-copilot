import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "spark"))

from spark.session import create_spark_session

spark = create_spark_session()

TABLE = "local.lakehouse.orders"

# Disable adaptive merging
spark.conf.set("spark.sql.adaptive.enabled", "false")

# Force one partition
spark.conf.set("spark.sql.shuffle.partitions", "1")

# Create many tiny writes
for i in range(100):

    print(f"Writing batch {i+1}/100")

    (
        spark.table(TABLE)
        .limit(5)
        .writeTo(TABLE)
        .append()
    )

spark.stop()

print("\nFinished creating small files.")