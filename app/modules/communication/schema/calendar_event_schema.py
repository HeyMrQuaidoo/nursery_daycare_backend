from pydantic import UUID4
from typing import Optional
from datetime import datetime

from app.modules.common.schema.base_schema import BaseSchema


class CalendarEventBase(BaseSchema):
    # id: UUID4
    # event_id: str
    title: str
    description: Optional[str] = None
    status: str
    event_type: str
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    organizer_id: UUID4


class CalendarEvent(BaseSchema):
    id: UUID4
    event_id: str
