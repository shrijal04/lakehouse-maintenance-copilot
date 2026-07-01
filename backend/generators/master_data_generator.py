from sqlalchemy import text

from generators.database import engine
from generators.seed_data import CATEGORIES, BRANDS, STORES


def seed_master_data():

    with engine.begin() as conn:

        # Categories
        for category in CATEGORIES:
            conn.execute(
                text("""
                    INSERT INTO categories(category_name)
                    VALUES (:name)
                    ON CONFLICT (category_name)
                    DO NOTHING
                """),
                {"name": category}
            )

        # Brands
        for brand in BRANDS:
            conn.execute(
                text("""
                    INSERT INTO brands(
                        brand_name,
                        headquarters_country
                    )
                    VALUES(
                        :name,
                        :country
                    )
                    ON CONFLICT (brand_name)
                    DO NOTHING
                """),
                {
                    "name": brand["name"],
                    "country": brand["country"]
                }
            )

        # Stores
        for store in STORES:
            conn.execute(
                text("""
                    INSERT INTO stores(
                        store_name,
                        city,
                        country,
                        manager_name,
                        opened_date
                    )
                    VALUES(
                        :store_name,
                        :city,
                        :country,
                        :manager,
                        CURRENT_DATE
                    )
                    ON CONFLICT (store_name)
                    DO NOTHING
                """),
                {
                    "store_name": store["store_name"],
                    "city": store["city"],
                    "country": store["country"],
                    "manager": store["manager"]
                }
            )

    print("Master data seeded successfully.")