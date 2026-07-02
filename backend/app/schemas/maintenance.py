from pydantic import BaseModel


class MaintenanceRequest(BaseModel):
    database: str
    target: str


class MaintenanceConfirmation(BaseModel):
    confirmation_id: str
    confirm: bool
    database: str
    target: str


class ConfirmationResponse(BaseModel):
    confirmation_required: bool
    confirmation_id: str
    database: str
    target: str
    message: str