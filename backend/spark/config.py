from pathlib import Path
from dotenv import load_dotenv
import os

# Project root (backend/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load backend/.env
load_dotenv(BASE_DIR / ".env")

POSTGRES = {
    "url": f"jdbc:postgresql://{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}",
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "driver": "org.postgresql.Driver",
}

WAREHOUSE_PATH = str(BASE_DIR / "spark" / "warehouse")

JDBC_JAR = str(BASE_DIR / "spark" / "jars" / "postgresql-42.7.11.jar")