import random

from faker import Faker
from sqlalchemy import text

from generators.database import engine
from generators.repository import get_brands, get_categories
from generators.seed_data import PRODUCT_CATALOG

fake = Faker()

random.seed(42)
Faker.seed(42)


def generate_product(product, brand_map, category_map):

    created_at = fake.date_time_between(
        start_date="-180d",
        end_date="-30d"
    )

    updated_at = fake.date_time_between(
        start_date=created_at,
        end_date="now"
    )

    return {
        "product_name": product["name"],
        "category_id": category_map[product["category"]],
        "brand_id": brand_map[product["brand"]],
        "price": round(random.uniform(100, 3500), 2),
        "stock_quantity": random.randint(10, 250),
        "supplier_name": fake.company(),
        "is_active": random.random() > 0.05,
        "created_at": created_at,
        "updated_at": updated_at,
    }


def seed_products():

    brand_map = get_brands()
    category_map = get_categories()

    with engine.begin() as conn:

        for product in PRODUCT_CATALOG:

            data = generate_product(
                product,
                brand_map,
                category_map
            )

            conn.execute(
                text("""
                    INSERT INTO products (
                        product_name,
                        category_id,
                        brand_id,
                        price,
                        stock_quantity,
                        supplier_name,
                        is_active,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        :product_name,
                        :category_id,
                        :brand_id,
                        :price,
                        :stock_quantity,
                        :supplier_name,
                        :is_active,
                        :created_at,
                        :updated_at
                    )
                    ON CONFLICT (product_name)
                    DO NOTHING;
                """),
                data
            )

    print("Products seeded successfully.")