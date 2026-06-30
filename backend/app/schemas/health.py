from pydantic import BaseModel


class HealthResponse(BaseModel):
    table: str
    snapshot_count: int
    data_file_count: int
    average_file_kb: float
    total_size_mb: float