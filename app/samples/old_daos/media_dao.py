from uuid import UUID
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List, Dict, Optional, Union

# models
from app.models.entity_media import EntityMedia
from app.models.media import Media as MediaModel

# utils
from app.utils.response import DAOResponse

# services
from app.services.upload_service import MediaUploaderService

# daos
from app.dao.resources.base_dao import BaseDAO
from app.dao.entities.entity_media_dao import EntityMediaDAO

# schemas
from app.schema.media import (
    MediaBase,
    Media,
    MediaCreateSchema,
    MediaResponse,
    MediaUpdateSchema,
)


class MediaDAO(BaseDAO[MediaModel]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = MediaModel
        self.primary_key = "media_id"
        self.entity_media_dao = EntityMediaDAO()

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    @override
    async def get_all(
        self, db_session: AsyncSession, offset=0, limit=100
    ) -> DAOResponse[List[MediaResponse]]:
        result = await super().get_all(
            db_session=db_session, offset=offset, limit=limit
        )

        return DAOResponse[List[MediaResponse]](
            success=True, data=[MediaResponse.from_orm_model(r) for r in result]
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

            # extract base information
            media_info = self.extract_model_data(obj_in, MediaCreateSchema)

            # process media information
            media_info = await self.upload_and_process_media(media_info, media_store)

            # create new media
            new_media: Media = await super().create(
                db_session=db_session, obj_in=media_info
            )

            return DAOResponse[MediaResponse](
                success=True, data=MediaResponse.from_orm_model(new_media)
            )
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"{str(e)}")

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
            entity_data = obj_in.model_dump()

            # extract base information
            media_info = self.extract_model_data(entity_data, Media)

            if "content_url" in media_info:
                media_info = await self.upload_and_process_media(
                    media_info, media_store
                )

            # update media info
            existing_media: Media = await super().update(
                db_session=db_session, db_obj=db_obj, obj_in=MediaBase(**media_info)
            )

            return DAOResponse[MediaResponse](
                success=True, data=MediaResponse.from_orm_model(existing_media)
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

    async def add_entity_media(
        self,
        db_session: AsyncSession,
        entity_id: str,
        media_info: Union[List[Media | MediaBase] | Media | MediaBase],
        entity_model: Union[str | None] = None,
        entity_assoc_id: Union[UUID | None] = None,
    ) -> Optional[List[EntityMedia]]:
        try:
            results = []
            entity_model_name = entity_model if entity_model else self.model.__name__
            media_info = media_info if isinstance(media_info, list) else [media_info]

            for media_item in media_info:
                media_item: Union[MediaBase | Media] = media_item
                # Check if the entity already exists
                existing_media_item = await self.query(
                    db_session=db_session,
                    filters={
                        **media_item.model_dump(
                            exclude=[
                                "content_url",
                                "is_thumbnail",
                                "caption",
                                "description",
                            ]
                        )
                    },
                    single=True,
                )

                if existing_media_item:
                    # update existing media
                    # obj_data = self.extract_model_data(media_item.model_dump(), Media)
                    # obj_data["media_id"] = existing_media_item.media_id

                    # media_data = Media(**obj_data)

                    media_upload: DAOResponse = await self.update(
                        db_session=db_session,
                        db_obj=existing_media_item,
                        obj_in=media_item,
                    )
                else:
                    # create new media
                    media_upload: DAOResponse[MediaResponse] = await self.create(
                        db_session=db_session,
                        obj_in=media_item.model_dump(),
                        media_store=entity_model_name.lower(),
                    )

                # check for content url success and
                # check if media was uploaded correctly
                if not media_upload.success:
                    raise Exception(str(media_upload.error))

                # links an entity to a particular media
                entity_media = await self.associate_media_with_entity(
                    db_session=db_session,
                    media_id=media_upload.data.media_id,
                    entity_assoc_id=entity_assoc_id or entity_id,
                    entity_model=entity_model_name,
                )

                # append the media upload results
                results.append(entity_media)

            return results
        except NoResultFound:
            pass
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Media DAO Error: {str(e)}")

    async def associate_media_with_entity(
        self,
        db_session: AsyncSession,
        media_id: UUID,
        entity_assoc_id: Union[UUID | None] = None,
        entity_model: Union[str | None] = None,
    ) -> EntityMedia:
        entity_media_object = {
            "entity_type": entity_model if entity_model else self.model.__name__,
            "media_assoc_id": entity_assoc_id,
            "media_id": media_id,
        }

        # check if entity media linkage exists
        result = await self.entity_media_dao.query(
            db_session=db_session, filters={**entity_media_object}, single=True
        )

        # create entity media linkage if it doesn't exist
        if not result:
            result = await self.entity_media_dao.create(
                db_session=db_session, obj_in=entity_media_object
            )

        return result.data
