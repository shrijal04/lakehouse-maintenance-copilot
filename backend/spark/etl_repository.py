from sqlalchemy import text
from database import engine


def get_last_run(pipeline_name: str):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT last_run_timestamp
                FROM etl_metadata
                WHERE pipeline_name = :pipeline
            """),
            {"pipeline": pipeline_name}
        )

        row = result.fetchone()

        if row:
            return row.last_run_timestamp

        return None


def update_last_run(pipeline_name: str, timestamp):

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE etl_metadata
                SET
                    last_run_timestamp = :ts,
                    status = 'SUCCESS',
                    updated_at = CURRENT_TIMESTAMP
                WHERE pipeline_name = :pipeline
            """),
            {
                "pipeline": pipeline_name,
                "ts": timestamp
            }
        )