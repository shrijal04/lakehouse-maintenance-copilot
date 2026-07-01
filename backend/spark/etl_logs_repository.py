from sqlalchemy import text

from spark.database import engine


def log_etl_run(
    pipeline_name,
    start_time,
    end_time,
    status,
    orders_processed,
    order_items_processed,
    message
):

    with engine.begin() as conn:

        conn.execute(

            text("""

            INSERT INTO etl_logs (

                pipeline_name,
                start_time,
                end_time,
                status,
                orders_processed,
                order_items_processed,
                message

            )

            VALUES (

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
                "message": message

            }

        )