from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.schemas.maintenance import ConfirmationResponse,MaintenanceConfirmation
from app.services.maintenance_service import (
    get_orders_health,
    request_orders_maintenance,
    confirm_orders_maintenance,
)

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