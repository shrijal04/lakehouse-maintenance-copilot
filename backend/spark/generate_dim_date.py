from datetime import date, timedelta

from pyspark.sql import Row

from session import create_spark_session

spark = create_spark_session()

start_date = date(2025, 1, 1)
end_date = date(2027, 12, 31)

rows = []

current = start_date

while current <= end_date:

    rows.append(
        Row(
            date_key=int(current.strftime("%Y%m%d")),
            full_date=current,
            year=current.year,
            quarter=(current.month - 1) // 3 + 1,
            month=current.month,
            month_name=current.strftime("%B"),
            day=current.day,
            day_name=current.strftime("%A"),
            week_of_year=current.isocalendar().week,
            is_weekend=current.weekday() >= 5,
        )
    )

    current += timedelta(days=1)

df = spark.createDataFrame(rows)

(
    df.writeTo("local.lakehouse.dim_date")
    .using("iceberg")
    .createOrReplace()
)

print(f"Inserted {df.count()} dates.")

spark.stop()