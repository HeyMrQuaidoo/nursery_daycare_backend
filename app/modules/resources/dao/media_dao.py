from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Optional, Union

# core
from app.core.response import DAOResponse

# models
from app.modules.resources.models.media import Media

# dao
from app.modules.common.dao.base_dao import BaseDAO

# services
from app.services.upload_service import MediaUploaderService

# schemas
from app.modules.resources.schema.mixins.media_mixin import MediaBase
from app.modules.resources.schema.media_schema import (
    MediaCreateSchema,
    MediaResponse,
    MediaUpdateSchema,
)


class MediaDAO(BaseDAO[Media]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Media
        self.detail_mappings = {}

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="media_id",
        )

    @override
    async def create(
        self,
        db_session: AsyncSession,
        obj_in: Union[MediaCreateSchema | Dict],
        media_store: str = None,
    ) -> DAOResponse:
        try:
            # specify calling class
            media_store = self.model.__name__ if media_store is None else media_store

            # process media information
            media_info = await self.upload_and_process_media(
                obj_in.model_dump(), media_store
            )

            # create new media
            new_media: Media = await super().create(
                db_session=db_session, obj_in=media_info
            )

            return new_media if isinstance(new_media, DAOResponse) else new_media
        except Exception as e:
            await db_session.rollback()
            raise e
            # return DAOResponse(success=False, error=f"{str(e)}")

    @override
    async def update(
        self,
        db_session: AsyncSession,
        db_obj: Media,
        obj_in: MediaUpdateSchema,
        media_store: str = None,
    ) -> DAOResponse[MediaResponse]:
        try:
            # specify calling class
            media_store = self.model.__name__ if media_store is None else media_store

            # get the entity dump info
            media_info = obj_in.model_dump()

            if "content_url" in media_info:
                media_info = await self.upload_and_process_media(
                    media_info, media_store
                )

            # update media info
            existing_media: Media = await super().update(
                db_session=db_session, db_obj=db_obj, obj_in=MediaBase(**media_info)
            )

            return (
                existing_media
                if isinstance(existing_media, DAOResponse)
                else existing_media
            )
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[MediaResponse](success=False, error=f"{str(e)}")

    async def upload_and_process_media(
        self, media_info: Dict[str, Any], media_store: str
    ) -> Dict[str, Any]:
        base64_data = media_info.get("content_url")

        uploader_service = MediaUploaderService(
            base64_image=base64_data,
            file_name=media_info.get("media_name"),
            media_type=media_store.lower(),
        )

        upload_response = uploader_service.upload()

        if not upload_response.success:
            raise Exception(str(upload_response.error))

        media_info["content_url"] = upload_response.data["content_url"]

        media_type = uploader_service.get_image_type()
        user_provided_media_type = media_info.get("media_type")

        if media_type and media_type == user_provided_media_type:
            media_info["media_type"] = media_type
        else:
            media_info["media_type"] = user_provided_media_type

        return media_info
