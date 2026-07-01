from datetime import datetime
import random

from sqlalchemy import text

from generators.database import Database
from generators.repository import Repository
from generators.order_generator import OrderGenerator


class BusinessDaySimulator:

    STATUS_FLOW = {
        "Pending": "Processing",
        "Processing": "Shipped",
        "Shipped": "Delivered",
        "Delivered": "Delivered",
        "Cancelled": "Cancelled",
    }

    def __init__(self):

        self.engine = Database().get_engine()
        self.repository = Repository()
        self.order_generator = OrderGenerator()

    # ---------------------------------------
    # Update Existing Orders
    # ---------------------------------------

    def update_existing_orders(self, update_count=5):

        existing_orders = self.repository.get_existing_orders()

        if len(existing_orders) < update_count:
            update_count = len(existing_orders)

        if update_count == 0:
            return 0

        selected = random.sample(existing_orders, update_count)

        with self.engine.begin() as conn:

            for order in selected:

                new_status = self.STATUS_FLOW.get(
                    order["status"],
                    order["status"],
                )

                conn.execute(
                    text("""
                        UPDATE orders
                        SET
                            status = :status,
                            updated_at = :updated_at
                        WHERE order_id = :order_id
                    """),
                    {
                        "status": new_status,
                        "updated_at": datetime.now(),
                        "order_id": order["order_id"],
                    },
                )

        return update_count

    # ---------------------------------------
    # Insert New Orders
    # ---------------------------------------

    def insert_new_orders(self, new_order_count=20):

        self.order_generator.insert_today_orders(new_order_count)

        return new_order_count

    # ---------------------------------------
    # Simulate Business Day
    # ---------------------------------------

    def simulate_business_day(self):

        print("=" * 60)
        print("Simulating Business Day")
        print("=" * 60)

        new_orders = self.insert_new_orders(20)

        updated_orders = self.update_existing_orders(5)

        print(f"Inserted Orders : {new_orders}")
        print(f"Updated Orders  : {updated_orders}")

        print("=" * 60)
        print("Business Day Simulation Completed")
        print("=" * 60)

        return {
            "status": "Success",
            "message": "Business day simulated successfully.",
            "new_orders": new_orders,
            "updated_orders": updated_orders,
            "simulation_time": datetime.now().isoformat(),
        }


if __name__ == "__main__":

    simulator = BusinessDaySimulator()

    result = simulator.simulate_business_day()

    print(result)