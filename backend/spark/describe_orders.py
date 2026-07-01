from manager import get_spark

spark = get_spark()

spark.sql("""
DESCRIBE TABLE local.lakehouse.orders
""").show(truncate=False)

spark.stop()