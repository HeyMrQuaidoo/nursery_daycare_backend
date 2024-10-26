from uuid import UUID
from typing import Annotated, Optional
from pydantic import ConfigDict, constr

# schema
from app.modules.common.schema.base_schema import BaseFaker
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.resources.enums.resource_enums import MediaType


class EntityMediaCreateSchema(BaseSchema):
    """
    Schema for creating an entity media association.

    Attributes:
        entity_media_id (Optional[UUID]): The unique identifier for the entity media association.
        entity_type (str): The type of the entity.
        media_id (UUID): The unique identifier for the media.
        media_assoc_id (UUID): The unique identifier for the media association.
    """

    entity_media_id: Optional[UUID] = None
    entity_type: Annotated[str, constr(max_length=50)]
    media_id: UUID
    media_assoc_id: UUID

    model_config = ConfigDict(from_attributes=True)


class MediaBase(BaseSchema):
    media_name: Optional[str] = None
    media_type: Optional[MediaType] = None
    content_url: Optional[str] = None
    is_thumbnail: Optional[bool] = False
    caption: Optional[str] = None
    description: Optional[str] = None


class Media(MediaBase):
    media_id: Optional[UUID]


class MediaInfoMixin:
    _media_name = BaseFaker.word()
    _media_type = BaseFaker.random_choices(
        ["image", "video", "audio", "document"], length=1
    )
    _content_url = BaseFaker.url()
    _is_thumbnail = BaseFaker.boolean()
    _caption = BaseFaker.sentence()
    _description = BaseFaker.text(max_nb_chars=200)

    _media_create_json = {
        "media_name": _media_name,
        "media_type": _media_type[0],
        "content_url": _content_url,
        "is_thumbnail": _is_thumbnail,
        "caption": _caption,
        "description": _description,
    }

    _media_update_json = {
        "media_name": _media_name,
        "media_type": _media_type[0],
        "content_url": _content_url,
        "is_thumbnail": _is_thumbnail,
        "caption": _caption,
        "description": _description,
    }
