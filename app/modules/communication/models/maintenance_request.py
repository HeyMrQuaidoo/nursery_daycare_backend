import uuid
import pytz
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import event, ForeignKey, DateTime, UUID, String, Text, Boolean

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.common.enums.common_enums import PriorityEnum
from app.modules.communication.enums.communication_enums import MaintenanceStatusEnum


class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"
    MNT_REQ_PREFIX = "TSK"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    task_number: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String, default=MaintenanceStatusEnum.pending, nullable=True
    )
    priority: Mapped[str] = mapped_column(
        String, default=PriorityEnum.medium, nullable=True
    )
    requested_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    # property_unit_assoc_id: Mapped[Optional[uuid.UUID]] = mapped_column(
    #     UUID(as_uuid=True),
    #     ForeignKey("property_unit_assoc.property_unit_assoc_id"),
    #     nullable=True,
    # )
    scheduled_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), nullable=True
    )
    completed_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), nullable=True
    )
    is_emergency: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # user
    user: Mapped["User"] = relationship(
        "User", back_populates="maintenance_requests", lazy="selectin"
    )


@event.listens_for(MaintenanceRequest, "before_insert")
def receive_before_insert(mapper, connection, target: MaintenanceRequest):
    if not target.task_number:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        target.task_number = f"{MaintenanceRequest.MNT_REQ_PREFIX}{current_time_str}"


@event.listens_for(MaintenanceRequest, "after_insert")
def receive_after_insert(mapper, connection, target: MaintenanceRequest):
    if not target.task_number:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        target.task_number = f"{MaintenanceRequest.MNT_REQ_PREFIX}{current_time_str}"
        connection.execute(
            target.__table__.update()
            .where(target.__table__.c.id == target.id)
            .values(task_number=target.task_number)
        )
