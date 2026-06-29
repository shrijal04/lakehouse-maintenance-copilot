from session import create_spark_session

spark = create_spark_session()

spark.sql("""
SELECT COUNT(*)
FROM local.lakehouse.orders
""").show()

spark.stop()