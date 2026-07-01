from datetime import datetime

from sqlalchemy import text

from spark.database import DatabaseManager


class ETLRepository:

    def __init__(self):

        self.engine = DatabaseManager().get_engine()

    # ==========================================================
    # ETL Metadata
    # ==========================================================

    def get_last_run(self, pipeline_name: str):

        with self.engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT last_run_timestamp
                    FROM etl_metadata
                    WHERE pipeline_name = :pipeline
                """),
                {
                    "pipeline": pipeline_name
                },
            )

            row = result.fetchone()

            if row:
                return row.last_run_timestamp

            return datetime(2000, 1, 1)

    def update_last_run(self, pipeline_name: str, timestamp):

        with self.engine.begin() as conn:

            conn.execute(
                text("""
                    INSERT INTO etl_metadata
                    (
                        pipeline_name,
                        last_run_timestamp,
                        status,
                        updated_at
                    )
                    VALUES
                    (
                        :pipeline,
                        :ts,
                        'SUCCESS',
                        CURRENT_TIMESTAMP
                    )

                    ON CONFLICT (pipeline_name)

                    DO UPDATE SET

                        last_run_timestamp = EXCLUDED.last_run_timestamp,

                        status = 'SUCCESS',

                        updated_at = CURRENT_TIMESTAMP
                """),
                {
                    "pipeline": pipeline_name,
                    "ts": timestamp,
                },
            )

    # ==========================================================
    # ETL Logging
    # ==========================================================

    def log_etl_run(
        self,
        pipeline_name,
        start_time,
        end_time,
        status,
        orders_processed,
        order_items_processed,
        message,
    ):

        with self.engine.begin() as conn:

            conn.execute(
                text("""
                    INSERT INTO etl_logs
                    (
                        pipeline_name,
                        start_time,
                        end_time,
                        status,
                        orders_processed,
                        order_items_processed,
                        message
                    )
                    VALUES
                    (
                        :pipeline,
                        :start,
                        :end,
                        :status,
                        :orders,
                        :items,
                        :message
                    )
                """),
                {
                    "pipeline": pipeline_name,
                    "start": start_time,
                    "end": end_time,
                    "status": status,
                    "orders": orders_processed,
                    "items": order_items_processed,
                    "message": message,
                },
            )

    # ==========================================================
    # Dashboard Metrics
    # ==========================================================

    def get_order_count_between(self, start_date, end_date):

        with self.engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT COUNT(*)
                    FROM bronze_orders
                    WHERE order_date >= :start_date
                      AND order_date <= :end_date
                """),
                {
                    "start_date": start_date,
                    "end_date": end_date,
                },
            )

            return result.scalar()

    def get_customer_count_between(self, start_date, end_date):

        with self.engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT COUNT(DISTINCT customer_id)
                    FROM bronze_orders
                    WHERE order_date >= :start_date
                      AND order_date <= :end_date
                """),
                {
                    "start_date": start_date,
                    "end_date": end_date,
                },
            )

            return result.scalar()

    def get_total_sales_between(self, start_date, end_date):

        with self.engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT COALESCE(SUM(total_amount), 0)
                    FROM bronze_orders
                    WHERE order_date >= :start_date
                      AND order_date <= :end_date
                """),
                {
                    "start_date": start_date,
                    "end_date": end_date,
                },
            )

            return float(result.scalar() or 0)

    def get_top_products_between(self, start_date, end_date):

        with self.engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT
                        product_name,
                        SUM(quantity) AS qty
                    FROM bronze_orders
                    WHERE order_date >= :start_date
                      AND order_date <= :end_date
                    GROUP BY product_name
                    ORDER BY qty DESC
                    LIMIT 5
                """),
                {
                    "start_date": start_date,
                    "end_date": end_date,
                },
            )

            return [
                {
                    "product": row.product_name,
                    "quantity": row.qty,
                }
                for row in result
            ]