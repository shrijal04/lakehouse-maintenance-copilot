from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.schemas.maintenance import (
    ConfirmationResponse,
    MaintenanceConfirmation,
)

from app.services.maintenance_service import (
    get_orders_health,
    get_order_items_health,
    get_orders_issues,
    get_order_items_issues,
    get_orders_health_history,
    get_order_items_health_history,
    request_orders_maintenance,
    confirm_orders_maintenance,
)

from app.services.dashboard_service import get_dashboard_metrics
from app.services.iceberg_services import get_all_tables

router = APIRouter(
    prefix="/lakehouse",
    tags=["Lakehouse"],
)


# =====================================================
# Dashboard
# =====================================================

@router.get("/dashboard")
def dashboard():
    return get_dashboard_metrics()

@router.get("/tables")
def iceberg_tables():
    return get_all_tables()


# =====================================================
# Orders Health
# =====================================================

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
    return get_orders_health_history()


# =====================================================
# Order Items Health
# =====================================================

@router.get(
    "/order-items/health",
    response_model=HealthResponse,
)
def order_items_health():
    return get_order_items_health()


@router.get("/order-items/issues")
def order_items_issues():
    return get_order_items_issues()


@router.get("/order-items/history")
def order_items_history():
    return get_order_items_health_history()


# =====================================================
# Maintenance
# =====================================================

@router.post(
    "/orders/maintenance/request",
    response_model=ConfirmationResponse,
)
def request_maintenance():
    return request_orders_maintenance()


@router.post("/orders/maintenance/confirm")
def confirm_maintenance(
    request: MaintenanceConfirmation,
):
    return confirm_orders_maintenance(
        request.confirmation_id,
        request.confirm,
    )