from uuid import UUID
from typing import List, Union
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession


# enums
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum

# models
from app.modules.forms.models.entity_questionnaire import EntityQuestionnaire

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
from app.modules.auth.schema.mixins.user_mixin import UserBaseMixin


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
                questionnaires = await self.dao.query(
                    db_session, filters={"published": True}
                )

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
                    db_session,
                    filters={"publish_for_registration": True},
                    order_by=["created_at"],
                )

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

        @self.router.get("/responses/")
        async def get_user_entity_questionnaire_data(
            request: Request,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(self.get_db),
        ):
            # Query entity questionnaires where entity_type is 'user'
            stmt = (
                select(EntityQuestionnaire)
                .options(
                    selectinload(EntityQuestionnaire.question),
                    selectinload(EntityQuestionnaire.answer),
                    selectinload(EntityQuestionnaire.questionnaire),
                )
                .where(EntityQuestionnaire.entity_type == EntityTypeEnum.user)
            )

            result = await db_session.execute(stmt)
            entity_questionnaires = result.scalars().all()

            # Structure data into the desired JSON format, grouped by user_id
            users_data = {}
            for entity_q in entity_questionnaires:
                # Get user_id
                user_id = str(entity_q.entity_id)

                # Initialize user entry if it doesn't exist
                if user_id not in users_data:
                    users_data[user_id] = {
                        "user_id": UserBaseMixin.get_user_info(entity_q.user),
                        "questionnaires": [],
                    }

                # Get questionnaire details
                questionnaire_id = str(entity_q.questionnaire_id)

                # Check if this questionnaire has already been added for this user
                questionnaire_entry = next(
                    (
                        q
                        for q in users_data[user_id]["questionnaires"]
                        if q["questionnaire_id"] == questionnaire_id
                    ),
                    None,
                )

                if not questionnaire_entry:
                    # Add a new questionnaire entry for this user
                    questionnaire_entry = {
                        "title": entity_q.questionnaire.title,
                        "description": entity_q.questionnaire.description,
                        "questions": [],
                        "publish_for_registration": entity_q.questionnaire.publish_for_registration,
                        "published": entity_q.questionnaire.published,
                        "created_at": str(entity_q.questionnaire.created_at),
                        "updated_at": str(entity_q.questionnaire.updated_at),
                        "number_of_responses": entity_q.questionnaire.number_of_responses,
                        "questionnaire_id": questionnaire_id,
                        "read": True,  # Initially assume all answers are read
                    }
                    users_data[user_id]["questionnaires"].append(questionnaire_entry)

                # Prepare question data
                question_data = {
                    "question_id": str(entity_q.question_id),
                    "questionnaire_id": questionnaire_id,
                    "content": entity_q.question.content,
                    "question_type": entity_q.question.question_type.value,
                    "answers": [],
                }

                # Prepare answer data if exists
                if entity_q.answer_id:
                    answer_data = {
                        "answer_id": str(entity_q.answer_id),
                        "questionnaire_id": questionnaire_id,
                        "question_id": str(entity_q.question_id),
                        "answer_type": entity_q.answer.answer_type.value,
                        "content": entity_q.answer.content,
                        "mark_as_read": entity_q.mark_as_read,
                    }
                    question_data["answers"].append(answer_data)

                    # Update the read status if any answer is unread
                    if not entity_q.mark_as_read:
                        questionnaire_entry["read"] = False

                # Check if question is already added to avoid duplicates
                if question_data not in questionnaire_entry["questions"]:
                    questionnaire_entry["questions"].append(question_data)

            # Convert the result to a list of user data
            result = list(users_data.values())

            return (
                result
                if isinstance(result, DAOResponse)
                else DAOResponse(success=True, data=result)
            )

        @self.router.put("/{questionnaire_id}/responses/{user_id}")
        async def update_user_entity_questionnaire_data(
            questionnaire_id: Union[str | UUID],
            user_id: Union[str | UUID],
            item: QuestionnaireUpdateSchema,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(self.get_db),
        ):
            try:
                update_stmt = (
                    update(EntityQuestionnaire)
                    .where(
                        EntityQuestionnaire.questionnaire_id == questionnaire_id,
                        EntityQuestionnaire.entity_id == user_id,
                        EntityQuestionnaire.entity_type == EntityTypeEnum.user,
                    )
                    .values(item.model_dump(exclude_none=True))
                )
                await db_session.execute(update_stmt)
                await db_session.commit()

            except Exception as e:
                await db_session.rollback()
                raise Exception(f"Failed to mark questionnaire as read: {str(e)}")

            stmt = (
                select(EntityQuestionnaire)
                .options(
                    selectinload(EntityQuestionnaire.question),
                    selectinload(EntityQuestionnaire.answer),
                    selectinload(EntityQuestionnaire.questionnaire),
                )
                .where(
                    EntityQuestionnaire.entity_type == EntityTypeEnum.user,
                    EntityQuestionnaire.entity_id == user_id,
                    EntityQuestionnaire.questionnaire_id == questionnaire_id,
                )
            )

            result = await db_session.execute(stmt)
            entity_questionnaires = result.scalars().all()

            if not entity_questionnaires:
                raise RecordNotFoundException(
                    model="EntityQuestionnaire",
                    id=f"{questionnaire_id} for user {user_id}",
                )

            users_data = {}

            for entity_q in entity_questionnaires:
                # Get user_id
                user_id = str(entity_q.entity_id)

                # Initialize user entry if it doesn't exist
                if user_id not in users_data:
                    users_data[user_id] = {
                        "user_id": UserBaseMixin.get_user_info(entity_q.user),
                        "questionnaires": [],
                    }

                # Get questionnaire details
                questionnaire_id = str(entity_q.questionnaire_id)

                # Check if this questionnaire has already been added for this user
                questionnaire_entry = next(
                    (
                        q
                        for q in users_data[user_id]["questionnaires"]
                        if q["questionnaire_id"] == questionnaire_id
                    ),
                    None,
                )

                if not questionnaire_entry:
                    # Add a new questionnaire entry for this user
                    questionnaire_entry = {
                        "title": entity_q.questionnaire.title,
                        "description": entity_q.questionnaire.description,
                        "questions": [],
                        "publish_for_registration": entity_q.questionnaire.publish_for_registration,
                        "published": entity_q.questionnaire.published,
                        "created_at": str(entity_q.questionnaire.created_at),
                        "updated_at": str(entity_q.questionnaire.updated_at),
                        "number_of_responses": entity_q.questionnaire.number_of_responses,
                        "questionnaire_id": questionnaire_id,
                        "read": True,  # Initially assume all answers are read
                    }
                    users_data[user_id]["questionnaires"].append(questionnaire_entry)

                # Prepare question data
                question_data = {
                    "question_id": str(entity_q.question_id),
                    "questionnaire_id": questionnaire_id,
                    "content": entity_q.question.content,
                    "question_type": entity_q.question.question_type.value,
                    "answers": [],
                }

                # Prepare answer data if exists
                if entity_q.answer_id:
                    answer_data = {
                        "answer_id": str(entity_q.answer_id),
                        "questionnaire_id": questionnaire_id,
                        "question_id": str(entity_q.question_id),
                        "answer_type": entity_q.answer.answer_type.value,
                        "content": entity_q.answer.content,
                        "mark_as_read": entity_q.mark_as_read,
                    }
                    question_data["answers"].append(answer_data)

                    # Update the read status if any answer is unread
                    if not entity_q.mark_as_read:
                        questionnaire_entry["read"] = False

                # Check if question is already added to avoid duplicates
                if question_data not in questionnaire_entry["questions"]:
                    questionnaire_entry["questions"].append(question_data)

            return DAOResponse(success=True, data=users_data[str(user_id)])

        @self.router.get("/responses/{user_id}")
        async def get_user_entity_questionnaire_data_by_id(
            user_id: Union[str | UUID],
            request: Request,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(self.get_db),
        ):
            # Query entity questionnaires where entity_type is 'user'
            stmt = (
                select(EntityQuestionnaire)
                .options(
                    selectinload(EntityQuestionnaire.question),
                    selectinload(EntityQuestionnaire.answer),
                    selectinload(EntityQuestionnaire.questionnaire),
                )
                .where(
                    EntityQuestionnaire.entity_type == EntityTypeEnum.user,
                    EntityQuestionnaire.entity_id == user_id,
                )
            )

            result = await db_session.execute(stmt)
            entity_questionnaires = result.scalars().all()

            # Structure data into the desired JSON format, grouped by user_id
            users_data = {}
            for entity_q in entity_questionnaires:
                # Get user_id
                user_id = str(entity_q.entity_id)

                # Initialize user entry if it doesn't exist
                if user_id not in users_data:
                    users_data[user_id] = {
                        "user_id": UserBaseMixin.get_user_info(entity_q.user),
                        "questionnaires": [],
                    }

                # Get questionnaire details
                questionnaire_id = str(entity_q.questionnaire_id)

                # Check if this questionnaire has already been added for this user
                questionnaire_entry = next(
                    (
                        q
                        for q in users_data[user_id]["questionnaires"]
                        if q["questionnaire_id"] == questionnaire_id
                    ),
                    None,
                )

                if not questionnaire_entry:
                    # Add a new questionnaire entry for this user
                    questionnaire_entry = {
                        "title": entity_q.questionnaire.title,
                        "description": entity_q.questionnaire.description,
                        "questions": [],
                        "publish_for_registration": entity_q.questionnaire.publish_for_registration,
                        "published": entity_q.questionnaire.published,
                        "created_at": str(entity_q.questionnaire.created_at),
                        "updated_at": str(entity_q.questionnaire.updated_at),
                        "number_of_responses": entity_q.questionnaire.number_of_responses,
                        "questionnaire_id": questionnaire_id,
                        "read": True,  # Initially assume all answers are read
                    }
                    users_data[user_id]["questionnaires"].append(questionnaire_entry)

                # Prepare question data
                question_data = {
                    "question_id": str(entity_q.question_id),
                    "questionnaire_id": questionnaire_id,
                    "content": entity_q.question.content,
                    "question_type": entity_q.question.question_type.value,
                    "answers": [],
                }

                # Prepare answer data if exists
                if entity_q.answer_id:
                    answer_data = {
                        "answer_id": str(entity_q.answer_id),
                        "questionnaire_id": questionnaire_id,
                        "question_id": str(entity_q.question_id),
                        "answer_type": entity_q.answer.answer_type.value,
                        "content": entity_q.answer.content,
                        "mark_as_read": entity_q.mark_as_read,
                    }
                    question_data["answers"].append(answer_data)

                    # Update the read status if any answer is unread
                    if not entity_q.mark_as_read:
                        questionnaire_entry["read"] = False

                # Check if question is already added to avoid duplicates
                if question_data not in questionnaire_entry["questions"]:
                    questionnaire_entry["questions"].append(question_data)

            # Convert the result to a list of user data
            result = list(users_data.values())

            return (
                result
                if isinstance(result, DAOResponse)
                else DAOResponse(success=True, data=result)
            )
