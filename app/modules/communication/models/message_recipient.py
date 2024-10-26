import uuid
import pytz
from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Boolean, UUID

from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class MessageRecipient(Base):
    __tablename__ = "message_recipient"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    recipient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id")
    )
    recipient_group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    message_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("message.message_id")
    )
    is_read: Mapped[Optional[bool]] = mapped_column(Boolean)
    msg_send_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )

    # users
    recipient: Mapped["User"] = relationship(
        "User", back_populates="received_messages", lazy="selectin"
    )

    # messages
    message: Mapped["Message"] = relationship(
        "Message", back_populates="recipients", lazy="selectin"
    )
