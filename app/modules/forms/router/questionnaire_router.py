from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Query, Request

# dao
from app.modules.forms.dao.questionnaire_dao import QuestionnaireDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schema
from app.modules.common.schema.schemas import QuestionnaireSchema
from app.modules.forms.schema.questionnaire_schema import (
    QuestionnaireCreateSchema,
    QuestionnaireUpdateSchema,
)

# core
from app.core.response import DAOResponse
from app.core.errors import CustomException, RecordNotFoundException, IntegrityError


class QuestionnaireRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        QuestionnaireSchema["create_schema"] = QuestionnaireCreateSchema
        QuestionnaireSchema["update_schema"] = QuestionnaireUpdateSchema
        self.dao: QuestionnaireDAO = QuestionnaireDAO(
            excludes=["entity_questionnaires"]
        )

        super().__init__(
            dao=self.dao, schemas=QuestionnaireSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        @self.router.get("/published/")
        async def published_questionnaires(
            request: Request,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(self.get_db),
        ):
            try:
                print("HERE")
                questionnaires = await self.dao.query(
                    db_session, filters={"published": True}
                )
                if not questionnaires:
                    raise RecordNotFoundException(model=self.model_schema.__name__)
                meta = await self.dao.build_pagination_meta(
                    request=request,
                    limit=limit,
                    offset=offset,
                    db_session=db_session,
                    filter_condition={"published": True},
                )

                if isinstance(questionnaires, DAOResponse):
                    if hasattr(questionnaires, "meta") and getattr(
                        questionnaires, "meta"
                    ):
                        meta_data = questionnaires.meta
                        meta.update(meta_data)
                    questionnaires.set_meta(meta)

                return (
                    questionnaires
                    if isinstance(questionnaires, DAOResponse)
                    else DAOResponse(success=True, data=questionnaires, meta=meta)
                )
            except RecordNotFoundException as e:
                raise e
            except IntegrityError as e:
                raise e
            except Exception as e:
                raise CustomException(e)

        @self.router.get("/unpublished/")
        async def unpublished_questionnaires(
            request: Request,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(self.get_db),
        ):
            try:
                questionnaires = await self.dao.query(
                    db_session, filters={"published": False}
                )
                if not questionnaires:
                    raise RecordNotFoundException(model=self.model_schema.__name__)
                meta = await self.dao.build_pagination_meta(
                    request=request,
                    limit=limit,
                    offset=offset,
                    db_session=db_session,
                    filter_condition={"published": False},
                )

                if isinstance(questionnaires, DAOResponse):
                    if hasattr(questionnaires, "meta") and getattr(
                        questionnaires, "meta"
                    ):
                        meta_data = questionnaires.meta
                        meta.update(meta_data)
                    questionnaires.set_meta(meta)

                return (
                    questionnaires
                    if isinstance(questionnaires, DAOResponse)
                    else DAOResponse(success=True, data=questionnaires, meta=meta)
                )
            except RecordNotFoundException as e:
                raise e
            except IntegrityError as e:
                raise e
            except Exception as e:
                raise CustomException(e)

        @self.router.get("/onboarding/")
        async def onboarding_questionnaires(
            request: Request,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(self.get_db),
        ):
            try:
                questionnaires = await self.dao.query(
                    db_session, filters={"publish_for_registration": True}
                )
                if not questionnaires:
                    raise RecordNotFoundException(model=self.model_schema.__name__)
                meta = await self.dao.build_pagination_meta(
                    request=request,
                    limit=limit,
                    offset=offset,
                    db_session=db_session,
                    filter_condition={"publish_for_registration": True},
                )

                if isinstance(questionnaires, DAOResponse):
                    if hasattr(questionnaires, "meta") and getattr(
                        questionnaires, "meta"
                    ):
                        meta_data = questionnaires.meta
                        meta.update(meta_data)
                    questionnaires.set_meta(meta)

                return (
                    questionnaires
                    if isinstance(questionnaires, DAOResponse)
                    else DAOResponse(success=True, data=questionnaires, meta=meta)
                )
            except RecordNotFoundException as e:
                raise e
            except IntegrityError as e:
                raise e
            except Exception as e:
                raise CustomException(e)
