import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


class DatabaseManager:

    def __init__(self):

        load_dotenv()

        self.db_url = (
            f"postgresql+psycopg2://"
            f"{os.getenv('POSTGRES_USER')}:"
            f"{os.getenv('POSTGRES_PASSWORD')}@"
            f"{os.getenv('POSTGRES_HOST')}:"
            f"{os.getenv('POSTGRES_PORT')}/"
            f"{os.getenv('POSTGRES_DB')}"
        )

        self.engine = create_engine(self.db_url)

    def get_engine(self):

        return self.engine