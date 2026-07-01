from spark.manager import SparkManagerService


class TableDescriber:

    def __init__(self, table_name):

        self.spark = SparkManagerService()
        self.table_name = table_name

    def describe(self):

        self.spark.sql(f"""
            DESCRIBE TABLE {self.table_name}
        """).show(truncate=False)

    def stop(self):

        self.spark.stop()


def main():

    describer = TableDescriber(
        "local.lakehouse.orders"
    )

    describer.describe()

    describer.stop()


if __name__ == "__main__":
    main()