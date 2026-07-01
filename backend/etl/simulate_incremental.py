import random
from datetime import datetime

from sqlalchemy import text

from app.database import engine
from spark.etl_repository import get_last_run


class IncrementalDataSimulator:

    def __init__(self):

        self.engine = engine

    def random_timestamp(self, last_run: datetime):

        now = datetime.now()

        start = last_run.timestamp()
        end = now.timestamp()

        random_time = random.uniform(start, end)

        return datetime.fromtimestamp(random_time)

    def simulate_incremental_data(self):

        last_run = get_last_run("orders_incremental")

        updated_orders = 0
        inserted_orders = 0
        inserted_items = 0

        with self.engine.begin() as conn:

            # ==========================================================
            # Update Existing Orders
            # ==========================================================

            existing_orders = conn.execute(
                text("""
                    SELECT order_id
                    FROM orders
                    ORDER BY RANDOM()
                    LIMIT 10
                """)
            ).fetchall()

            for row in existing_orders:

                conn.execute(
                    text("""
                        UPDATE orders
                        SET
                            order_total = :total,
                            updated_at = :updated_at
                        WHERE order_id = :order_id
                    """),
                    {
                        "order_id": row.order_id,
                        "total": random.randint(100, 800),
                        "updated_at": self.random_timestamp(last_run),
                    },
                )

                updated_orders += 1

            # ==========================================================
            # Next IDs
            # ==========================================================

            next_order_id = conn.execute(
                text("""
                    SELECT COALESCE(MAX(order_id), 0)
                    FROM orders
                """)
            ).scalar() + 1

            next_item_id = conn.execute(
                text("""
                    SELECT COALESCE(MAX(order_item_id), 0)
                    FROM order_items
                """)
            ).scalar() + 1

            # ==========================================================
            # Insert New Orders
            # ==========================================================

            for i in range(5):

                order_time = self.random_timestamp(last_run)

                order_id = next_order_id + i

                conn.execute(
                    text("""
                        INSERT INTO orders
                        (
                            order_id,
                            customer_id,
                            order_date,
                            status,
                            order_total,
                            created_at,
                            updated_at
                        )
                        VALUES
                        (
                            :order_id,
                            :customer_id,
                            CURRENT_DATE,
                            'Completed',
                            :order_total,
                            :created_at,
                            :updated_at
                        )
                    """),
                    {
                        "order_id": order_id,
                        "customer_id": random.randint(1, 100),
                        "order_total": random.randint(150, 900),
                        "created_at": order_time,
                        "updated_at": order_time,
                    },
                )

                inserted_orders += 1

                # ======================================================
                # Insert Order Items
                # ======================================================

                items = random.randint(1, 4)

                for _ in range(items):

                    conn.execute(
                        text("""
                            INSERT INTO order_items
                            (
                                order_item_id,
                                order_id,
                                product_id,
                                quantity,
                                unit_price,
                                created_at,
                                updated_at
                            )
                            VALUES
                            (
                                :item_id,
                                :order_id,
                                :product_id,
                                :quantity,
                                :unit_price,
                                :created_at,
                                :updated_at
                            )
                        """),
                        {
                            "item_id": next_item_id,
                            "order_id": order_id,
                            "product_id": random.randint(1, 50),
                            "quantity": random.randint(1, 5),
                            "unit_price": random.randint(20, 250),
                            "created_at": order_time,
                            "updated_at": order_time,
                        },
                    )

                    next_item_id += 1
                    inserted_items += 1

        print("=" * 60)
        print("Incremental Data Simulation")
        print("=" * 60)
        print(f"Updated Orders      : {updated_orders}")
        print(f"Inserted Orders     : {inserted_orders}")
        print(f"Inserted Items      : {inserted_items}")
        print("=" * 60)

        return {
            "updated_orders": updated_orders,
            "inserted_orders": inserted_orders,
            "inserted_items": inserted_items,
        }


def main():

    simulator = IncrementalDataSimulator()

    result = simulator.simulate_incremental_data()

    print(result)


if __name__ == "__main__":
    main()