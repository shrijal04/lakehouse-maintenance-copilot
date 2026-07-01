import random
from datetime import datetime

from faker import Faker
from sqlalchemy import text

from generators.database import Database
from generators.repository import (
    Repository
)
from generators.config import ORDER_STATUS, PAYMENT_METHODS, CITIES


class OrderGenerator:

    def __init__(self, seed=42):
        self.fake = Faker()
        random.seed(seed)
        Faker.seed(seed)

        self.repository= Repository()

        self.customers = None
        self.stores = None
        self.products = None

    # -------------------------
    # Public methods
    # -------------------------

    def seed_orders(self, order_count=500):
        self._load_reference_data()

        order_item_count = 0

        with Database().get_engine().begin() as conn:
            for _ in range(order_count):
                order_date = self.fake.date_time_between(
                    start_date="-180d",
                    end_date="now"
                )

                order_id, item_count = self._create_order(conn, order_date)
                order_item_count += item_count

        print(f"Inserted {order_count} orders.")
        print(f"Inserted {order_item_count} order items.")

    def insert_today_orders(self, order_count=10):
        """
        Inserts today's orders so Incremental ETL can detect them.
        """
        self._load_reference_data()

        order_item_count = 0

        with Database().get_engine().begin() as conn:
            for _ in range(order_count):
                now = datetime.now()

                order_id, item_count = self._create_order(conn, now)
                order_item_count += item_count

        print(f"Inserted {order_count} new orders.")
        print(f"Inserted {order_item_count} order items.")

    # -------------------------
    # Private methods
    # -------------------------

    def _load_reference_data(self):
        self.customers = self.repository.get_customer_ids()
        self.stores = self.repository.get_store_ids()
        self.products = self.repository.get_products()

    def _create_order(self, conn, order_date):
        """
        Builds order items, inserts the order, then inserts its
        order items. Returns (order_id, item_count).
        """
        customer_id = random.choice(self.customers)
        store_id = random.choice(self.stores)
        shipping_city = random.choice(CITIES)

        status = random.choices(
            ORDER_STATUS,
            weights=[5, 10, 20, 60, 5]
        )[0]

        payment_method = random.choice(PAYMENT_METHODS)

        order_items, total_amount = self._build_order_items()

        order_id = self._insert_order(
            conn,
            customer_id=customer_id,
            store_id=store_id,
            order_date=order_date,
            status=status,
            payment_method=payment_method,
            total_amount=total_amount,
            shipping_city=shipping_city,
        )

        self._insert_order_items(conn, order_id, order_items, order_date)

        return order_id, len(order_items)

    def _build_order_items(self):
        """
        Selects 1-5 unique products and computes line totals.
        Returns (order_items, total_amount).
        """
        order_items = []
        total_amount = 0

        selected_products = random.sample(
            self.products,
            random.randint(1, 5)
        )

        for product in selected_products:
            quantity = random.randint(1, 3)

            discount = random.choice([
                0,
                0,
                0,
                5,
                10,
                15,
                20
            ])

            unit_price = float(product["price"])

            line_total = (
                unit_price
                * quantity
                * (1 - discount / 100)
            )

            total_amount += line_total

            order_items.append({
                "product_id": product["product_id"],
                "quantity": quantity,
                "unit_price": unit_price,
                "discount": discount,
                "line_total": round(line_total, 2)
            })

        return order_items, total_amount

    def _insert_order(
        self,
        conn,
        customer_id,
        store_id,
        order_date,
        status,
        payment_method,
        total_amount,
        shipping_city,
    ):
        order_result = conn.execute(
            text("""
                INSERT INTO orders (
                    customer_id,
                    order_date,
                    status,
                    payment_method,
                    total_amount,
                    shipping_city,
                    shipping_country,
                    created_at,
                    updated_at,
                    store_id
                )
                VALUES (
                    :customer_id,
                    :order_date,
                    :status,
                    :payment_method,
                    :total_amount,
                    :shipping_city,
                    :shipping_country,
                    :created_at,
                    :updated_at,
                    :store_id
                )
                RETURNING order_id
            """),
            {
                "customer_id": customer_id,
                "order_date": order_date,
                "status": status,
                "payment_method": payment_method,
                "total_amount": round(total_amount, 2),
                "shipping_city": shipping_city,
                "shipping_country": "Nepal",
                "created_at": order_date,
                "updated_at": order_date,
                "store_id": store_id
            }
        )

        return order_result.scalar_one()

    def _insert_order_items(self, conn, order_id, order_items, order_date):
        for item in order_items:
            conn.execute(
                text("""
                    INSERT INTO order_items (
                        order_id,
                        product_id,
                        quantity,
                        unit_price,
                        discount,
                        line_total,
                        created_at
                    )
                    VALUES (
                        :order_id,
                        :product_id,
                        :quantity,
                        :unit_price,
                        :discount,
                        :line_total,
                        :created_at
                    )
                """),
                {
                    "order_id": order_id,
                    "product_id": item["product_id"],
                    "quantity": item["quantity"],
                    "unit_price": item["unit_price"],
                    "discount": item["discount"],
                    "line_total": item["line_total"],
                    "created_at": order_date
                }
            )