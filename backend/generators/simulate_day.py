from datetime import datetime
import random

from sqlalchemy import text

from database import engine
from repository import get_existing_orders
from order_generator import insert_today_orders


STATUS_FLOW = {
    "Pending": "Processing",
    "Processing": "Shipped",
    "Shipped": "Delivered",
    "Delivered": "Delivered",
    "Cancelled": "Cancelled"
}


def update_existing_orders(update_count=5):

    existing_orders = get_existing_orders()

    if len(existing_orders) < update_count:
        update_count = len(existing_orders)

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
                    "order_id": order["order_id"]
                }
            )

    print(f"Updated {update_count} existing orders.")


def insert_new_orders():

    insert_today_orders(800)


def main():

    insert_new_orders()

    update_existing_orders(5)

    print("Simulated one business day.")


if __name__ == "__main__":
    main()