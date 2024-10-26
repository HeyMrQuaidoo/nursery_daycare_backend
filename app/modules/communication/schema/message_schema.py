from pydantic import UUID4
from typing import Optional
from datetime import datetime

from app.modules.common.schema.base_schema import BaseSchema


class MessageBase(BaseSchema):
    message_id: UUID4
    subject: Optional[str] = None
    sender_id: Optional[UUID4] = None
    message_body: Optional[str] = None
    parent_message_id: Optional[UUID4] = None
    thread_id: Optional[UUID4] = None
    is_draft: Optional[bool] = None
    is_notification: Optional[bool] = None
    is_reminder: Optional[bool] = None
    is_scheduled: Optional[bool] = None
    is_read: Optional[bool] = None
    date_created: datetime
    scheduled_date: datetime
    next_remind_date: Optional[datetime] = None
    reminder_frequency_id: Optional[int] = None


class MessageRecipientBase(BaseSchema):
    id: UUID4
    recipient_id: UUID4
    recipient_group_id: Optional[UUID4] = None
    message_id: UUID4
    is_read: Optional[bool] = None
    msg_send_date: datetime
