from pydantic import UUID4
from typing import Optional
from datetime import datetime


from app.modules.common.schema.base_schema import BaseSchema


class TourBase(BaseSchema):
    # tour_booking_id: UUID4
    name: str
    email: str
    phone_number: str
    tour_type: str
    status: str
    tour_date: datetime
    property_unit_assoc_id: UUID4
    user_id: Optional[UUID4] = None


class Tour(BaseSchema):
    tour_booking_id: UUID4
