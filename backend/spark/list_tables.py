from session import create_spark_session

spark = create_spark_session()

spark.sql("SHOW TABLES IN local.lakehouse").show(truncate=False)

spark.stop()