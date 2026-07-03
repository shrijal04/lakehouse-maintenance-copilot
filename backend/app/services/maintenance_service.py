from maintenance.health_metric import HealthService
from maintenance.run_maintenance import Maintenance

from spark.manager import SparkManager

from app.services.health_history_service import HealthRepository
from app.services.confirmation_service import confirmation_manager


class MaintenanceService:

    def __init__(self):

        self.spark = SparkManager().get_spark()

        self.health = HealthService(self.spark)

        self.health_repository = HealthRepository()

        self.maintenance_runner = Maintenance(self.spark)

        # Use the singleton confirmation manager
        self.confirmation = confirmation_manager

    # ---------------------------------------------------
    # Helpers
    # ---------------------------------------------------

    def get_table_name(
        self,
        database: str,
        target: str,
    ):
        return f"local.{database}.{target}"

    # ---------------------------------------------------
    # Health
    # ---------------------------------------------------

    def get_table_health(
        self,
        database: str,
        target: str,
    ):

        if target == "both":

            results = []

            for table in [
                "orders",
                "order_items",
            ]:

                table_name = self.get_table_name(
                    database,
                    table,
                )

                metrics = self.health.get_table_health(
                    table_name,
                )

                self.health_repository.save_health_metrics(
                    metrics
                )

                results.append(metrics)

            return results

        table_name = self.get_table_name(
            database,
            target,
        )

        metrics = self.health.get_table_health(
            table_name,
        )

        self.health_repository.save_health_metrics(
            metrics
        )

        return metrics

    # ---------------------------------------------------
    # Health History
    # ---------------------------------------------------

    def get_table_health_history(
        self,
        database: str,
        target: str,
    ):

        if target == "both":

            return {
                "orders": self.health_repository.get_health_history(
                    self.get_table_name(
                        database,
                        "orders",
                    )
                ),
                "order_items": self.health_repository.get_health_history(
                    self.get_table_name(
                        database,
                        "order_items",
                    )
                ),
            }

        table_name = self.get_table_name(
            database,
            target,
        )

        return self.health_repository.get_health_history(
            table_name
        )

    # ---------------------------------------------------
    # Issues
    # ---------------------------------------------------

    def get_table_issues(
        self,
        database: str,
        target: str,
    ):

        if target == "both":

            results = []

            for table in [
                "orders",
                "order_items",
            ]:

                table_name = self.get_table_name(
                    database,
                    table,
                )

                metrics = self.health.get_table_health(
                    table_name,
                )

                results.append(
                    {
                        "table": table,
                        "issues": self.health.get_health_issues(
                            metrics
                        ),
                    }
                )

            return results

        table_name = self.get_table_name(
            database,
            target,
        )

        metrics = self.health.get_table_health(
            table_name,
        )

        return self.health.get_health_issues(
            metrics
        )

    # ---------------------------------------------------
    # Request Maintenance
    # ---------------------------------------------------

    def request_maintenance(
        self,
        database: str,
        target: str,
    ):

        confirmation_id = (
            self.confirmation.create_confirmation(
                database=database,
                table=target,
                action="maintenance",
            )
        )

        return {
            "confirmation_required": True,
            "confirmation_id": confirmation_id,
            "database": database,
            "target": target,
            "message": (
                "Running maintenance will:\n"
                "- Rewrite small data files\n"
                "- Rewrite manifest files\n"
                "- Expire old snapshots\n"
                "- Remove orphan files\n\n"
                f"Database: {database}\n"
                f"Table: {target}\n\n"
                "Do you want to continue?"
            ),
        }

    # ---------------------------------------------------
    # Confirm Maintenance
    # ---------------------------------------------------

    def confirm_maintenance(
        self,
        confirmation_id: str,
        confirm: bool,
        database: str,
        target: str,
    ):

        if not confirm:

            self.confirmation.remove_confirmation(
                confirmation_id
            )

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

        result = self.maintenance_runner.run_maintenance(
            database=database,
            target=target,
        )

        return {
            "status": "success",
            "result": result,
        }