from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.schemas.maintenance import ConfirmationResponse,MaintenanceConfirmation
from app.services.maintenance_service import (
    get_orders_health,
    get_orders_issues,
    request_orders_maintenance,
    confirm_orders_maintenance,
)
from app.services.health_history_service import get_health_history
TABLE = "local.lakehouse.orders"
router = APIRouter(
    prefix="/lakehouse",
    tags=["Lakehouse"],
)


@router.get(
    "/orders/health",
    response_model=HealthResponse,
)
def orders_health():
    return get_orders_health()

@router.get("/orders/issues")
def orders_issues():
    return get_orders_issues()

@router.get("/orders/history")
def orders_history():
    return get_health_history(TABLE)

@router.post(
    "/orders/maintenance/request",
    response_model=ConfirmationResponse,
)
def request_maintenance():
    return request_orders_maintenance()


@router.post("/orders/maintenance/confirm")
def confirm_maintenance(request: MaintenanceConfirmation):
    return confirm_orders_maintenance(
        request.confirmation_id,
        request.confirm,
    )