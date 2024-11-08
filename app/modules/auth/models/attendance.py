import uuid
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, func, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

# models
from app.modules.common.models.model_base import BaseModel as Base


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    attendance_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True
    )
    check_in_time: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    check_out_time: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    date_stamp: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )

    # users
    user: Mapped["User"] = relationship(
        "User",
        back_populates="attendance_logs",
        lazy="selectin",
    )
