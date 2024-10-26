from uuid import UUID
from pydantic import constr
from datetime import datetime
from typing import Annotated, Optional

# schemas
from app.modules.common.schema.base_schema import BaseSchema


class BillableBase(BaseSchema):
    billable_assoc_id: Optional[UUID] = None
    billable_type: str


class Billable(BillableBase):
    billable_assoc_id: Optional[UUID] = None
    billable_type: str


class EntityBillableBase(BaseSchema):
    payment_type_id: int
    entity_id: UUID
    entity_type: Annotated[str, constr(max_length=50)]
    billable_id: UUID
    billable_type: Annotated[str, constr(max_length=50)]
    billable_amount: Optional[int | str] = None
    apply_to_units: Optional[bool] = False
    start_period: Optional[datetime] = None
    end_period: Optional[datetime] = None


class EntityBillable(EntityBillableBase):
    entity_billable_id: Optional[UUID] = None
