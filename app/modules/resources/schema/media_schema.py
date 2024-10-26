from uuid import UUID
from datetime import date
from typing import Annotated, Optional
from pydantic import ConfigDict, constr

# schema mixin
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.resources.schema.mixins.media_mixin import MediaBase, MediaInfoMixin

# models
from app.modules.resources.models.media import Media as MediaModel


class MediaCreateSchema(MediaBase, MediaInfoMixin):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={"example": MediaInfoMixin._media_create_json},
    )


class MediaUpdateSchema(MediaBase):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={"example": MediaInfoMixin._media_update_json},
    )


class MediaResponse(MediaBase):
    media_id: Optional[UUID] = None

    @classmethod
    def model_validate(cls, media: MediaModel) -> "MediaResponse":
        return cls(
            media_id=media.media_id,
            media_name=media.media_name,
            media_type=media.media_type,
            content_url=media.content_url,
            is_thumbnail=media.is_thumbnail,
            caption=media.caption,
            description=media.description,
        ).model_dump()


class EntityMediaCreateSchema(BaseSchema):
    entity_media_id: Optional[UUID] = None
    entity_type: Annotated[str, constr(max_length=50)]
    media_id: UUID
    media_assoc_id: UUID

    model_config = ConfigDict(from_attributes=True)
