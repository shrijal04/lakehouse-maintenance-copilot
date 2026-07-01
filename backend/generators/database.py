from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()


class Database:

    _engine = None

    def __init__(self):

        if Database._engine is None:

            db_url = (
                f"postgresql+psycopg2://"
                f"{os.getenv('POSTGRES_USER')}:"
                f"{os.getenv('POSTGRES_PASSWORD')}@"
                f"{os.getenv('POSTGRES_HOST')}:"
                f"{os.getenv('POSTGRES_PORT')}/"
                f"{os.getenv('POSTGRES_DB')}"
            )

            Database._engine = create_engine(db_url)

    def get_engine(self):
        return Database._engine