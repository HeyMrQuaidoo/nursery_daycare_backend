import uuid
from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class BillableAssoc(Base):
    __tablename__ = "billable_assoc"

    billable_assoc_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    billing_type: Mapped[str] = mapped_column(String)

    __mapper_args__ = {
        "polymorphic_on": billing_type,
        "polymorphic_identity": "billable_assoc",
    }
