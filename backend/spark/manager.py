from spark.session import create_spark_session

spark = None


def get_spark():
    global spark

    try:
        if spark is None:
            spark = create_spark_session()
        else:
            # Check whether the Spark session is still alive
            spark.sparkContext.applicationId

    except Exception:
        # Spark was stopped, so create a new one
        spark = create_spark_session()

    return spark