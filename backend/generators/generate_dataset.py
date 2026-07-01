from generators.master_data_generator import seed_master_data
from generators.product_generator import seed_products
from generators.customer_generator import seed_customers
from generators.order_generator import seed_orders


def main():

    seed_master_data()

    seed_products()

    seed_customers(100)

    seed_orders(500)

    print("Dataset initialized successfully.")


if __name__ == "__main__":
    main()