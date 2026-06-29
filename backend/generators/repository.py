from sqlalchemy import text
from database import engine


# ==========================
# Master Data Lookups
# ==========================

def get_categories():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT category_id, category_name
                FROM categories
            """)
        )

        return {
            row.category_name: row.category_id
            for row in result
        }


def get_brands():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT brand_id, brand_name
                FROM brands
            """)
        )

        return {
            row.brand_name: row.brand_id
            for row in result
        }


def get_stores():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT store_id, store_name
                FROM stores
            """)
        )

        return {
            row.store_name: row.store_id
            for row in result
        }


# ==========================
# Transaction Data Lookups
# ==========================

def get_customer_ids():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT customer_id
                FROM customers
            """)
        )

        return [row.customer_id for row in result]


def get_store_ids():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT store_id
                FROM stores
            """)
        )

        return [row.store_id for row in result]


def get_products():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT product_id, price
                FROM products
            """)
        )

        return [
            {
                "product_id": row.product_id,
                "price": float(row.price)
            }
            for row in result
        ]