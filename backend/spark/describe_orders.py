from session import create_spark_session

spark = create_spark_session()

spark.sql("""
DESCRIBE TABLE local.lakehouse.orders
""").show(truncate=False)

spark.stop()