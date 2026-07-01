from datetime import datetime
import random

from sqlalchemy import text

from database import engine
from generators.repository import get_existing_orders
from generators.order_generator import insert_today_orders


STATUS_FLOW = {
    "Pending": "Processing",
    "Processing": "Shipped",
    "Shipped": "Delivered",
    "Delivered": "Delivered",
    "Cancelled": "Cancelled",
}


def update_existing_orders(update_count=5):

    existing_orders = get_existing_orders()

    if len(existing_orders) < update_count:
        update_count = len(existing_orders)

    if update_count == 0:
        return 0

    selected = random.sample(existing_orders, update_count)

    with engine.begin() as conn:

        for order in selected:

            new_status = STATUS_FLOW.get(
                order["status"],
                order["status"]
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


def insert_new_orders(new_order_count=20):

    insert_today_orders(new_order_count)

    return new_order_count


def simulate_business_day():

    print("=" * 60)
    print("Simulating Business Day")
    print("=" * 60)

    new_orders = insert_new_orders(20)

    updated_orders = update_existing_orders(5)

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


def main():

    result = simulate_business_day()

    print(result)


if __name__ == "__main__":
    main()