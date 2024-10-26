import uuid
from typing import Optional, List
from sqlalchemy import Enum, String, UUID, Boolean, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

# Base model
from app.modules.common.models.model_base import BaseModel as Base

# Enums
from app.modules.resources.enums.resource_enums import MediaType


class Media(Base):
    __tablename__ = "media"

    media_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    media_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    media_type: Mapped[Optional[MediaType]] = mapped_column(
        Enum(MediaType), nullable=True
    )
    content_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_thumbnail: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    caption: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    entity_media: Mapped[List["EntityMedia"]] = relationship(
        "EntityMedia",
        back_populates="media",
        overlaps="media",
        lazy="selectin",
    )


# Register model outside the class definition
Base.setup_model_dynamic_listener("media", Media)
