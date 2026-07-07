from apscheduler.schedulers.background import BackgroundScheduler

from spark.manager import SparkManagerService
from maintenance.health_metric import HealthService
from app.services.alert_cache import CURRENT_ALERTS

scheduler = BackgroundScheduler()


# --------------------------------------------------
# Scheduled Health Check
# --------------------------------------------------

def scheduled_health_check():
    """
    Runs a health check across all monitored tables and
    refreshes CURRENT_ALERTS with any detected issues.
    """

    print("\nRunning scheduled health check...")

    spark = SparkManagerService().get_spark()

    try:

        health_service = HealthService(spark)

        tables = [
            "local.silver.orders",
            "local.silver.order_items",
        ]

        alerts = []

        for table in tables:

            try:

                metrics = health_service.get_table_health(table)

                issues = health_service.get_health_issues(metrics)

                for issue in issues:

                    if issue["severity"] != "Healthy":

                        alerts.append(
                            {
                                "table": table,
                                "severity": issue["severity"],
                                "issue": issue["issue"],
                                "recommendation": issue["recommendation"],
                            }
                        )

            except Exception as e:
                print(f"[WARN] Health check failed for {table}: {e}")

        # ==========================================
        # Update CURRENT_ALERTS in place
        # ==========================================

        CURRENT_ALERTS.clear()
        CURRENT_ALERTS.extend(alerts)

        print(f"Health check complete. {len(alerts)} alert(s) found.")

    except Exception as e:
        print(f"[ERROR] Scheduled health check failed: {e}")




# --------------------------------------------------
# Scheduler Control
# --------------------------------------------------

def start_scheduler():

    if not scheduler.running:

        scheduler.add_job(
            scheduled_health_check,
            trigger="interval",
            minutes=5,
            id="health_check",
            replace_existing=True,
        )

        scheduler.start()

        # Run immediately so CURRENT_ALERTS isn't empty
        # for the first 5 minutes after startup
        scheduled_health_check()

        print("Health Scheduler Started")