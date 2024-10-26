import uuid
from sqlalchemy import Enum, CheckConstraint, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship

# Base model
from app.modules.common.models.model_base import BaseModel as Base

# Enums
from app.modules.resources.enums.resource_enums import MediaType
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum


class EntityMedia(Base):
    __tablename__ = "entity_media"

    entity_media_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    media_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("media.media_id"), nullable=False
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    entity_type: Mapped[EntityTypeEnum] = mapped_column(Enum(EntityTypeEnum))
    media_type: Mapped[MediaType] = mapped_column(
        Enum(MediaType), default=MediaType.other
    )

    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('user', 'contract')",
            name="check_entity_type_media",
        ),
    )

    __mapper_args__ = {"eager_defaults": True}

    media: Mapped["Media"] = relationship(
        "Media",
        back_populates="entity_media",
        overlaps="media",
        lazy="selectin",
    )

    @validates("entity_type", "entity_id")
    def validate_entity(self, key, value, **kwargs):
        if key == "entity_id":
            entity_id = value
            entity_type = kwargs.get("entity_type", self.entity_type)
        elif key == "entity_type":
            entity_type = value
            entity_id = self.entity_id

        entity_map = {
            EntityTypeEnum.user: ("users", "user_id"),
            EntityTypeEnum.contract: ("contract", "contract_id"),
        }

        if entity_type and EntityTypeEnum(str(entity_type)) in entity_map:
            super().validate_entity(
                entity_id=entity_id,
                entity_type=EntityTypeEnum(str(entity_type)),
                entity_map=entity_map,
            )
        return value
