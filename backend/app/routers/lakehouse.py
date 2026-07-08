from typing import List

from fastapi import APIRouter, Query
from fastapi.responses import FileResponse

from app.schemas.health import (
    HealthResponse,
    HealthIssue,
)
from app.schemas.maintenance import (
    ConfirmationResponse,
    MaintenanceConfirmation,
    MaintenanceRequest,
)

from app.services.dashboard_service import DashboardService
from app.services.iceberg_services import IcebergService
from app.services.maintenance_service import MaintenanceService
from app.services.ai_report_service import AIReportService


router = APIRouter(
    prefix="/lakehouse",
    tags=["Lakehouse"],
)

dashboard_service = DashboardService()
iceberg_service = IcebergService()
maintenance_service = MaintenanceService()
report_service = AIReportService()


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
# Generic Health
# =====================================================

@router.get(
    "/health",
    response_model=List[HealthResponse],
)
def table_health(
    database: str = Query(...),
    target: str = Query(...),
):
    return maintenance_service.get_table_health(
        database=database,
        target=target,
    )


# =====================================================
# Generic Issues
# =====================================================

@router.get(
    "/issues",
    response_model=List[HealthIssue],
)
def table_issues(
    database: str = Query(...),
    target: str = Query(...),
):
    return maintenance_service.get_table_issues(
        database=database,
        target=target,
    )


# =====================================================
# Generic History
# =====================================================

@router.get("/history")
def table_history(
    database: str = Query(...),
    target: str = Query(...),
):
    return maintenance_service.get_table_health_history(
        database=database,
        target=target,
    )


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
    return maintenance_service.request_maintenance(
        database=request.database,
        target=request.target,
    )


@router.post("/maintenance/confirm")
def confirm_maintenance(
    request: MaintenanceConfirmation,
):
    return maintenance_service.confirm_maintenance(
        confirmation_id=request.confirmation_id,
        confirm=request.confirm,
        database=request.database,
        target=request.target,
    )


# =====================================================
# AI Daily Report
# =====================================================

@router.get("/report")
def generate_report():
    return report_service.generate_daily_report()


# =====================================================
# Download PDF
# =====================================================

@router.get("/report/pdf")
def download_pdf():

    report = report_service.generate_daily_report()

    return FileResponse(
        report["pdf"],
        media_type="application/pdf",
        filename="Lakehouse_Daily_Report.pdf",
    )


# =====================================================
# Download DOCX
# =====================================================

@router.get("/report/docx")
def download_docx():

    report = report_service.generate_daily_report()

    return FileResponse(
        report["docx"],
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="Lakehouse_Daily_Report.docx",
    )