from spark.manager import SparkManagerService


class GoldInitialLoad:

    def __init__(self):

        self.spark = SparkManagerService().get_spark()

        self.spark.sql(
            "CREATE NAMESPACE IF NOT EXISTS local.lakehouse"
        )

    def create_daily_sales(self):

        print("\nCreating Daily Sales...")

        self.spark.sql("""

        CREATE OR REPLACE TABLE local.lakehouse.daily_sales
        USING iceberg AS

        SELECT
            order_date,
            COUNT(*) AS total_orders,
            SUM(total_amount) AS total_sales

        FROM local.silver.orders

        GROUP BY order_date

        """)

        print("Daily Sales created.")

    def create_store_sales(self):

        print("\nCreating Store Sales...")

        self.spark.sql("""

        CREATE OR REPLACE TABLE local.lakehouse.store_sales
        USING iceberg AS

        SELECT
            store_id,
            COUNT(*) AS total_orders,
            SUM(total_amount) AS total_sales

        FROM local.silver.orders

        GROUP BY store_id

        """)

        print("Store Sales created.")

    def create_customer_sales(self):

        print("\nCreating Customer Sales...")

        self.spark.sql("""

        CREATE OR REPLACE TABLE local.lakehouse.customer_sales
        USING iceberg AS

        SELECT
            customer_id,
            COUNT(*) AS total_orders,
            SUM(total_amount) AS total_sales

        FROM local.silver.orders

        GROUP BY customer_id

        """)

        print("Customer Sales created.")

    def run(self):

        self.create_daily_sales()

        self.create_store_sales()

        self.create_customer_sales()

        print("\nGold Initial Load Completed.")

        return {
            "status": "Success",
            "tables_created": 3,
        }


def main():

    pipeline = GoldInitialLoad()

    result = pipeline.run()

    print(result)


if __name__ == "__main__":

    main()