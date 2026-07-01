import random

from faker import Faker
from sqlalchemy import text

from generators.database import engine
from generators.repository import (
    get_customer_ids,
    get_store_ids,
    get_products,
)
from generators.config import ORDER_STATUS, PAYMENT_METHODS, CITIES

fake = Faker()

random.seed(42)
Faker.seed(42)


def seed_orders(order_count=500):

    customers = get_customer_ids()
    stores = get_store_ids()
    products = get_products()

    order_item_count = 0

    with engine.begin() as conn:

        for _ in range(order_count):

            customer_id = random.choice(customers)
            store_id = random.choice(stores)

            order_date = fake.date_time_between(
                start_date="-180d",
                end_date="now"
            )

            shipping_city = random.choice(CITIES)

            status = random.choices(
                ORDER_STATUS,
                weights=[5, 10, 20, 60, 5]
            )[0]

            payment_method = random.choice(PAYMENT_METHODS)

            order_items = []
            total_amount = 0

            # 1–5 unique products
            selected_products = random.sample(
                products,
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

            # -------------------------
            # Insert ONE order
            # -------------------------

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

            order_id = order_result.scalar_one()

            # -------------------------
            # Insert all order items
            # -------------------------

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

                order_item_count += 1

    print(f"Inserted {order_count} orders.")
    print(f"Inserted {order_item_count} order items.")

from datetime import datetime


def insert_today_orders(order_count=10):
    """
    Inserts today's orders so Incremental ETL can detect them.
    """

    customers = get_customer_ids()
    stores = get_store_ids()
    products = get_products()

    order_item_count = 0

    with engine.begin() as conn:

        for _ in range(order_count):

            now = datetime.now()

            customer_id = random.choice(customers)
            store_id = random.choice(stores)

            shipping_city = random.choice(CITIES)

            status = random.choices(
                ORDER_STATUS,
                weights=[5, 10, 20, 60, 5]
            )[0]

            payment_method = random.choice(PAYMENT_METHODS)

            order_items = []
            total_amount = 0

            selected_products = random.sample(
                products,
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

            order_result = conn.execute(
                text("""
                INSERT INTO orders(
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
                VALUES(
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
                    "order_date": now,
                    "status": status,
                    "payment_method": payment_method,
                    "total_amount": round(total_amount, 2),
                    "shipping_city": shipping_city,
                    "shipping_country": "Nepal",
                    "created_at": now,
                    "updated_at": now,
                    "store_id": store_id
                }
            )

            order_id = order_result.scalar_one()

            for item in order_items:

                conn.execute(
                    text("""
                    INSERT INTO order_items(
                        order_id,
                        product_id,
                        quantity,
                        unit_price,
                        discount,
                        line_total,
                        created_at
                    )
                    VALUES(
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
                        "created_at": now
                    }
                )

                order_item_count += 1

    print(f"Inserted {order_count} new orders.")
    print(f"Inserted {order_item_count} order items.")