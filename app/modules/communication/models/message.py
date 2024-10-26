import uuid
import pytz
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import relationship, backref, Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, Integer, String, Text, UUID, ForeignKey

from app.modules.common.models.model_base import BaseModel as Base


class Message(Base):
    __tablename__ = "message"

    message_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    subject: Mapped[Optional[str]] = mapped_column(String(128))
    sender_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id")
    )
    message_body: Mapped[Optional[str]] = mapped_column(Text)
    parent_message_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("message.message_id"), nullable=True
    )
    thread_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("message.message_id"), nullable=True
    )
    is_draft: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=False, nullable=True
    )
    is_notification: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=False, nullable=True
    )
    is_reminder: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=False, nullable=True
    )
    is_scheduled: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=False, nullable=True
    )
    is_read: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=False, nullable=True
    )
    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    scheduled_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    next_remind_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), nullable=True
    )
    reminder_frequency_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("reminder_frequency.reminder_frequency_id")
    )

    # reminders
    reminder_frequency: Mapped["ReminderFrequency"] = relationship(
        "ReminderFrequency", back_populates="messages"
    )

    # user
    sender: Mapped["User"] = relationship(
        "User", back_populates="sent_messages", lazy="selectin"
    )

    # recipients
    recipients: Mapped[List["MessageRecipient"]] = relationship(
        "MessageRecipient", back_populates="message", lazy="selectin"
    )

    # messages
    replies: Mapped[List["Message"]] = relationship(
        "Message",
        backref=backref("parent_message", remote_side=[message_id]),
        foreign_keys=[parent_message_id],
        cascade="all, delete-orphan",
    )
    thread: Mapped[List["Message"]] = relationship(
        "Message",
        remote_side=[message_id],
        backref=backref("thread_messages", foreign_keys=[thread_id]),
        foreign_keys=[thread_id],
    )
