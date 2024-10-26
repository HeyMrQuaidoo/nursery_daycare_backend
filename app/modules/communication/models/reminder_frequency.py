import uuid
from typing import List
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class ReminderFrequency(Base):
    __tablename__ = "reminder_frequency"

    reminder_frequency_id: Mapped[uuid.UUID] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(50))
    frequency: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="reminder_frequency"
    )
