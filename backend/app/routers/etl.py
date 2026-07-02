from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text

from app.database import engine

from spark.incremental_load import IncrementalETL
from spark.simulate_small_files import SmallFileSimulator
from generators.simulate_day import BusinessDaySimulator


# ---------------------------------------------------
# Request Models
# ---------------------------------------------------

class SmallFileRequest(BaseModel):
    database: str
    target: str
    batches: int = 100


router = APIRouter(
    prefix="/etl",
    tags=["ETL"],
)


@router.post("/run")
def run_etl():

    etl = IncrementalETL()

    return etl.run()


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

    simulator = BusinessDaySimulator()

    return simulator.simulate_business_day()


@router.post("/simulate-small-files")
def simulate_small_files(request: SmallFileRequest):

    simulator = SmallFileSimulator()

    return simulator.run(
        database=request.database,
        target=request.target,
        batches=request.batches,
    )