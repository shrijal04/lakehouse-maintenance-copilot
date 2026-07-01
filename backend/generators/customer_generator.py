import random

from faker import Faker
from sqlalchemy import text

from generators.database import engine

from generators.config import (
    ORDER_STATUS,
    PAYMENT_METHODS,
    CITIES,
)

fake = Faker()

random.seed(42)
Faker.seed(42)



def generate_customer():

    created_at = fake.date_time_between(
        start_date="-365d",
        end_date="-30d"
    )

    updated_at = fake.date_time_between(
        start_date=created_at,
        end_date="now"
    )

    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "phone": f"+97798{random.randint(10000000,99999999)}",
        "city": random.choice(CITIES),
        "country": "Nepal",
        "customer_segment": random.choices(
            CUSTOMER_SEGMENTS,
            weights=[70, 20, 10]
        )[0],
        "created_at": created_at,
        "updated_at": updated_at,
    }


def seed_customers(count=100):

    with engine.begin() as conn:

        for _ in range(count):

            customer = generate_customer()

            conn.execute(
                text("""
                    INSERT INTO customers(
                        first_name,
                        last_name,
                        email,
                        phone,
                        city,
                        country,
                        customer_segment,
                        created_at,
                        updated_at
                    )
                    VALUES(
                        :first_name,
                        :last_name,
                        :email,
                        :phone,
                        :city,
                        :country,
                        :customer_segment,
                        :created_at,
                        :updated_at
                    )
                    ON CONFLICT(email)
                    DO NOTHING;
                """),
                customer
            )

    print(f"{count} customers seeded.")