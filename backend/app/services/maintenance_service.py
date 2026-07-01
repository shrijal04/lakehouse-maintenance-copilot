from maintenance.health_metric import HealthService
from maintenance.run_maintenance import Maintenance

from spark.manager import SparkManager

from app.services.health_history_service import HealthRepository
from app.services.confirmation_service import ConfirmationManager


class MaintenanceService:

    TABLES = {
        "orders": "local.lakehouse.orders",
        "order_items": "local.lakehouse.order_items",
    }

    def __init__(self):

        self.spark = SparkManager().get_spark()
        self.health = HealthService(self.spark)
        self.health_repository = HealthRepository()
        self.maintenance_runner = Maintenance(self.spark)
        self.confirmation = ConfirmationManager()

    # ---------------------------------------------------
    # Health
    # ---------------------------------------------------

    def get_table_health(self, table_key: str):

        table_name = self.TABLES[table_key]

        metrics = self.health.get_table_health(
            table_name,
        )

        self.health_repository.save_health_metrics(metrics)

        return metrics

    def get_orders_health(self):
        return self.get_table_health("orders")

    def get_order_items_health(self):
        return self.get_table_health("order_items")

    # ---------------------------------------------------
    # Health History
    # ---------------------------------------------------

    def get_orders_health_history(self):
        return self.health_repository.get_health_history(
            self.TABLES["orders"]
        )

    def get_order_items_health_history(self):
        return self.health_repository.get_health_history(
            self.TABLES["order_items"]
        )

    # ---------------------------------------------------
    # Issues
    # ---------------------------------------------------

    def get_table_issues(self, table_key: str):

        metrics = self.health.get_table_health(
            self.TABLES[table_key],
        )

        return self.health.get_health_issues(metrics)

    def get_orders_issues(self):
        return self.get_table_issues("orders")

    def get_order_items_issues(self):
        return self.get_table_issues("order_items")

    # ---------------------------------------------------
    # Request Maintenance
    # ---------------------------------------------------

    def request_orders_maintenance(self):

        confirmation_id = self.confirmation.create_confirmation()

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
    # Confirm Maintenance
    # ---------------------------------------------------

    def confirm_orders_maintenance(
        self,
        confirmation_id: str,
        confirm: bool,
    ):

        if not confirm:
            return {
                "status": "cancelled",
                "message": "Maintenance cancelled.",
            }

        if not self.confirmation.is_valid_confirmation(
            confirmation_id
        ):
            return {
                "status": "error",
                "message": "Invalid or expired confirmation id.",
            }

        self.confirmation.remove_confirmation(
            confirmation_id
        )

        result = self.maintenance_runner.run_maintenance()

        return {
            "status": "success",
            "result": result,
        }