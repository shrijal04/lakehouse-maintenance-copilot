from fastapi import APIRouter
from sqlalchemy import text

from database import engine
from spark.incremental_load import run_incremental_load
from generators.simulate_day import simulate_business_day
from spark.simulate_small_files import simulate_small_files

router = APIRouter(
    prefix="/etl",
    tags=["ETL"]
)


@router.post("/run")
def run_etl():

    return run_incremental_load()


@router.get("/history")
def get_etl_history():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    id,
                    pipeline_name,
                    start_time,
                    end_time,
                    status,
                    orders_processed,
                    order_items_processed,
                    message
                FROM etl_logs
                ORDER BY start_time DESC
                LIMIT 50
            """)
        )

        return result.mappings().all()


@router.post("/simulate")
def simulate():

    return simulate_business_day()

@router.post("/simulate-small-files")
def simulate_small_files_endpoint():
    return simulate_small_files()