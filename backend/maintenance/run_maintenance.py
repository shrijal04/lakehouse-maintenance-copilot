import os
import sys

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "spark"))

from spark.session import create_spark_session

spark = create_spark_session()

TABLE = "local.lakehouse.orders"

print("=" * 60)
print("Running Iceberg Maintenance")
print("=" * 60)

# ---------------------------------------------------
# Rewrite small files
# ---------------------------------------------------

rewrite_df = spark.sql(f"""
CALL local.system.rewrite_data_files(
    table => '{TABLE}'
)
""")

print("\nRewrite Data Files Result")
rewrite_df.show(truncate=False)

rewrite = rewrite_df.first()

print("\nSummary")
print(f"Files rewritten : {rewrite.rewritten_data_files_count}")
print(f"Files added     : {rewrite.added_data_files_count}")
print(f"Bytes rewritten : {rewrite.rewritten_bytes_count}")

# ---------------------------------------------------
# Expire old snapshots
# ---------------------------------------------------

expire_df = spark.sql(f"""
CALL local.system.expire_snapshots(
    table => '{TABLE}',
    retain_last => 5
)
""")

print("\nExpire Snapshots Result")
expire_df.show(truncate=False)

expire = expire_df.first()

print("\nSummary")

for column in expire_df.columns:
    print(f"{column}: {getattr(expire, column)}")

spark.stop()

print("=" * 60)
print("Maintenance Finished")
print("=" * 60)