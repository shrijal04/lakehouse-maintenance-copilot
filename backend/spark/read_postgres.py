from session import create_spark_session
from config import POSTGRES

spark = create_spark_session()

df = (
    spark.read
    .format("jdbc")
    .option("url", POSTGRES["url"])
    .option("dbtable", "customers")
    .option("user", POSTGRES["user"])
    .option("password", POSTGRES["password"])
    .option("driver", POSTGRES["driver"])
    .load()
)

print("=" * 60)
print("Customers Table")
print("=" * 60)

df.show(10)

print(f"\nTotal Customers: {df.count()}")

spark.stop()