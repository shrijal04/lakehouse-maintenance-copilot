from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.schemas.maintenance import (
    ConfirmationResponse,
    MaintenanceConfirmation,
    MaintenanceRequest,
)

from app.services.dashboard_service import DashboardService
from app.services.iceberg_services import IcebergService
from app.services.maintenance_service import MaintenanceService


router = APIRouter(
    prefix="/lakehouse",
    tags=["Lakehouse"],
)

dashboard_service = DashboardService()
iceberg_service = IcebergService()
maintenance_service = MaintenanceService()


# =====================================================
# Dashboard
# =====================================================

@router.get("/dashboard")
def dashboard():
    return dashboard_service.get_dashboard_metrics()


@router.get("/tables")
def iceberg_tables():
    return iceberg_service.get_all_tables()


# =====================================================
# Orders Health
# =====================================================

@router.get(
    "/orders/health",
    response_model=HealthResponse,
)
def orders_health():
    return maintenance_service.get_orders_health()


@router.get("/orders/issues")
def orders_issues():
    return maintenance_service.get_orders_issues()


@router.get("/orders/history")
def orders_history():
    return maintenance_service.get_orders_health_history()


# =====================================================
# Order Items Health
# =====================================================

@router.get(
    "/order-items/health",
    response_model=HealthResponse,
)
def order_items_health():
    return maintenance_service.get_order_items_health()


@router.get("/order-items/issues")
def order_items_issues():
    return maintenance_service.get_order_items_issues()


@router.get("/order-items/history")
def order_items_history():
    return maintenance_service.get_order_items_health_history()


# =====================================================
# Maintenance
# =====================================================

@router.post(
    "/maintenance/request",
    response_model=ConfirmationResponse,
)
def request_maintenance(
    request: MaintenanceRequest,
):

    return maintenance_service.request_orders_maintenance(
        database=request.database,
        target=request.target,
    )


@router.post("/maintenance/confirm")
def confirm_maintenance(
    request: MaintenanceConfirmation,
):

    return maintenance_service.confirm_orders_maintenance(
        confirmation_id=request.confirmation_id,
        confirm=request.confirm,
        database=request.database,
        target=request.target,
    )