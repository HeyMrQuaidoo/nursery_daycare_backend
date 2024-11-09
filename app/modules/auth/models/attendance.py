import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, func, UUID, event, inspect

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


def parse_dates(mapper, connection, target):
    """Listener to convert start date and date_to to a datetime if it's provided as a string."""
    state = inspect(target)

    if state.attrs.check_in_time.history.has_changes():
        if isinstance(target.check_in_time, str):
            # Try to convert 'start date' string to datetime with or without microseconds
            try:
                target.check_in_time = datetime.strptime(
                    target.check_in_time, "%Y-%m-%dT%H:%M:%S.%f"
                )
            except ValueError:
                # Fallback to parsing without microseconds if not present
                target.check_in_time = datetime.strptime(
                    target.check_in_time, "%Y-%m-%dT%H:%M:%S"
                )

    if state.attrs.check_out_time.history.has_changes():
        if isinstance(target.check_out_time, str):
            # Try to convert 'start date' string to datetime with or without microseconds
            try:
                target.check_out_time = datetime.strptime(
                    target.check_out_time, "%Y-%m-%dT%H:%M:%S.%f"
                )
            except ValueError:
                # Fallback to parsing without microseconds if not present
                target.check_out_time = datetime.strptime(
                    target.check_out_time, "%Y-%m-%dT%H:%M:%S"
                )


event.listen(AttendanceLog, "before_insert", parse_dates)
event.listen(AttendanceLog, "before_update", parse_dates)
