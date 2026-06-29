from repository import get_brands, get_categories
from product_generator import generate_product
from seed_data import PRODUCT_CATALOG

brand_map = get_brands()
category_map = get_categories()

product = generate_product(
    PRODUCT_CATALOG[0],
    brand_map,
    category_map
)

print(product)