from pydantic import UUID4
from datetime import datetime
from typing import Optional

from app.modules.common.schema.base_schema import BaseSchema


class MaintenanceRequestBase(BaseSchema):
    # id: UUID4
    # task_number: str
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    requested_by: UUID4
    property_unit_assoc_id: Optional[UUID4] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    is_emergency: bool


class MaintenanceRequest(MaintenanceRequestBase):
    id: UUID4
    task_number: str
