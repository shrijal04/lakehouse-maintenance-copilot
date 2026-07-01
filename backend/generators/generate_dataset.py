from generators.config import (
    NUM_CUSTOMERS,
    NUM_PRODUCTS,
    NUM_ORDERS,
)

from generators.master_data_generator import (
    MasterDataGenerator,
)

from generators.product_generator import (
    ProductGenerator,
)

from generators.customer_generator import (
    CustomerGenerator,
)

from generators.order_generator import (
    OrderGenerator,
)


class DatasetGenerator:

    def __init__(self):

        self.master_generator = MasterDataGenerator()
        self.product_generator = ProductGenerator()
        self.customer_generator = CustomerGenerator()
        self.order_generator = OrderGenerator()

    def generate_dataset(self):

        print("=" * 60)
        print("Generating Dataset")
        print("=" * 60)

        self.master_generator.seed_master_data()

        self.product_generator.seed_products(NUM_PRODUCTS)

        self.customer_generator.seed_customers(NUM_CUSTOMERS)

        self.order_generator.seed_orders(NUM_ORDERS)

        print("=" * 60)
        print("Dataset initialized successfully.")
        print("=" * 60)


def main():

    generator = DatasetGenerator()

    generator.generate_dataset()


if __name__ == "__main__":
    main()