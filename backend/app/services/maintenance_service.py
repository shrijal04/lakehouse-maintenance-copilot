from maintenance.health_metric import (
    get_table_health,
    get_health_issues,
)
from maintenance.run_maintenance import run_maintenance
from spark.session import create_spark_session

from app.services.confirmation_service import (
    create_confirmation,
    is_valid_confirmation,
    remove_confirmation,
)

from app.services.health_history_service import (
    save_health_metrics,
    get_health_history,
)

TABLE = "local.lakehouse.orders"


# ---------------------------------------------------
# Health
# ---------------------------------------------------

def get_orders_health():
    spark = create_spark_session()

    try:
        metrics = get_table_health(spark, TABLE)

        # Save every health check for trend analysis
        save_health_metrics(metrics)

        return metrics

    finally:
        spark.stop()


# ---------------------------------------------------
# Health Trend
# ---------------------------------------------------

def get_orders_health_history():
    return get_health_history(TABLE)


# ---------------------------------------------------
# Issues
# ---------------------------------------------------

def get_orders_issues():
    spark = create_spark_session()

    try:
        metrics = get_table_health(spark, TABLE)
        return get_health_issues(metrics)

    finally:
        spark.stop()


# ---------------------------------------------------
# Step 1 : Request Maintenance
# ---------------------------------------------------

def request_orders_maintenance():

    confirmation_id = create_confirmation()

    return {
        "confirmation_required": True,
        "confirmation_id": confirmation_id,
        "message": (
            "Running maintenance will:\n"
            "- Rewrite small data files\n"
            "- Expire old snapshots\n"
            "- Remove orphan files\n\n"
            "Do you want to continue?"
        ),
    }


# ---------------------------------------------------
# Step 2 : Confirm Maintenance
# ---------------------------------------------------

def confirm_orders_maintenance(
    confirmation_id: str,
    confirm: bool,
):

    if not confirm:
        return {
            "status": "cancelled",
            "message": "Maintenance cancelled.",
        }

    if not is_valid_confirmation(confirmation_id):
        return {
            "status": "error",
            "message": "Invalid or expired confirmation id.",
        }

    remove_confirmation(confirmation_id)

    result = run_maintenance()

    return {
        "status": "success",
        "result": result,
    }