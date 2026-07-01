from maintenance.health_metric import (
    get_table_health,
    get_health_issues,
)

from maintenance.run_maintenance import run_maintenance

from spark.manager import get_spark

from app.services.confirmation_service import (
    create_confirmation,
    is_valid_confirmation,
    remove_confirmation,
)

from app.services.health_history_service import (
    save_health_metrics,
    get_health_history,
)

TABLES = {
    "orders": "local.lakehouse.orders",
    "order_items": "local.lakehouse.order_items",
}


# ---------------------------------------------------
# Health
# ---------------------------------------------------

def get_table_health_service(table_key: str):

    spark = get_spark()

    table_name = TABLES[table_key]

    metrics = get_table_health(
        spark,
        table_name,
    )

    save_health_metrics(metrics)

    return metrics


def get_orders_health():
    return get_table_health_service("orders")


def get_order_items_health():
    return get_table_health_service("order_items")


# ---------------------------------------------------
# Health History
# ---------------------------------------------------

def get_orders_health_history():
    return get_health_history(TABLES["orders"])


def get_order_items_health_history():
    return get_health_history(TABLES["order_items"])


# ---------------------------------------------------
# Issues
# ---------------------------------------------------

def get_table_issues(table_key: str):

    spark = get_spark()

    metrics = get_table_health(
        spark,
        TABLES[table_key],
    )

    return get_health_issues(metrics)


def get_orders_issues():
    return get_table_issues("orders")


def get_order_items_issues():
    return get_table_issues("order_items")


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
            "- Rewrite manifest files\n"
            "- Expire old snapshots\n"
            "- Remove orphan files\n\n"
            "Maintenance will run on BOTH fact tables:\n"
            "- local.lakehouse.orders\n"
            "- local.lakehouse.order_items\n\n"
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