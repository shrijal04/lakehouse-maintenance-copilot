from pydantic import BaseModel


class ConfirmationResponse(BaseModel):
    confirmation_id: str
    confirmation_required: bool
    message: str


class MaintenanceConfirmation(BaseModel):
    confirmation_id: str
    confirm: bool