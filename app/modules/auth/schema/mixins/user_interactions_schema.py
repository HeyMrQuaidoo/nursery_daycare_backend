from datetime import datetime
from pydantic import UUID4

from app.modules.common.schema.base_schema import BaseSchema


class UserInteractionsBase(BaseSchema):
    user_interaction_id: UUID4
    # user_id: UUID4
    employee_id: UUID4
    property_unit_assoc_id: UUID4
    contact_time: datetime
    contact_details: str
