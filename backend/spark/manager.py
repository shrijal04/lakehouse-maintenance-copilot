from spark.session import create_spark_session

spark = create_spark_session()


def get_spark():
    return spark