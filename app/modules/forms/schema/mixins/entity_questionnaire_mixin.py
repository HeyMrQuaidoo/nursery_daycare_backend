from uuid import UUID
from collections import defaultdict
from typing import Any, List, Optional, Union

# schema
from app.modules.forms.schema.mixins.answer_mixin import AnswerBase
from app.modules.forms.schema.mixins.question_mixin import QuestionBase
from app.modules.common.schema.base_schema import BaseSchema, BaseFaker
from app.modules.forms.schema.mixins.questionnaire_mixin import QuestionnaireBase

# enum
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum

# models
from app.modules.forms.models.entity_questionnaire import (
    EntityQuestionnaire as EntityQuestionnaireModel,
)


class EntityQuestionnaireMixin:
    _entity_id = BaseFaker.uuid4()
    _entity_type = BaseFaker.random_choices(["user", "questions"], length=1)
    _questionnaire_id = BaseFaker.uuid4()
    _question_id = BaseFaker.uuid4()
    _answer_id = BaseFaker.uuid4()
    _mark_as_read = BaseFaker.boolean()

    _entity_questionnaire_create_json = {
        "entity_id": _entity_id,
        "entity_type": _entity_type[0],
        "questionnaire_id": _questionnaire_id,
        "question_id": _question_id,
        "answer_id": _answer_id,
        "mark_as_read": _mark_as_read,
    }

    _entity_questionnaire_update_json = {
        "mark_as_read": _mark_as_read,
    }

    @classmethod
    def get_entity_questionnaire_info(
        cls,
        entity_questionnaire: Union[
            List["EntityQuestionnaireBase"] | "EntityQuestionnaireBase" | Any
        ],
    ) -> List[dict]:
        # print("HERE1")

        if not entity_questionnaire:
            return None
        # print(f"HERE2 {entity_questionnaire}")
        if not isinstance(entity_questionnaire, list):
            entity_questionnaire = [
                EntityQuestionnaireBase.model_validate(entity_questionnaire)
            ]

        # nested dictionary structure
        data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        # print("HERE3")
        # populate the nested structure with related details
        for eq in entity_questionnaire:
            # grouping by questionnaire_id, question_id, and answer_id
            data[eq.questionnaire_id][eq.question_id][eq.answer_id].append(
                {
                    "entity_id": eq.entity_id,
                    "entity_type": eq.entity_type,
                    "mark_as_read": eq.mark_as_read,
                    "entity_questionnaire_id": eq.entity_questionnaire_id,
                }
            )
        # print("HERE4")
        result = []
        for questionnaire_id, questions in data.items():
            # Fetch questionnaire details
            # print(f"HERE5 {entity_questionnaire}")
            # try:
            #     for eq in entity_questionnaire:
            #         print(eq.questionnaire)
            # except Exception as e:
            #     print(f"Error: {e}")

            #     for eq in entity_questionnaire:
            #         print(eq.questionnaire)
            questionnaire = next(
                (
                    eq.questionnaire
                    for eq in entity_questionnaire
                    if eq.questionnaire_id == questionnaire_id
                ),
                None,
            )
            # print("HERE6")
            questionnaire_dict = {
                "questionnaire_id": questionnaire_id,
                "title": questionnaire.title if questionnaire else None,
                "number_of_responses": questionnaire.number_of_responses
                if questionnaire
                else None,
                "publish_for_registration": questionnaire.publish_for_registration
                if questionnaire
                else None,
                "published": questionnaire.published if questionnaire else None,
                "description": questionnaire.description if questionnaire else None,
                "questions": [],
            }
            # print("HERE7")
            for question_id, answers in questions.items():
                # Fetch question details
                question = next(
                    (
                        eq.question
                        for eq in entity_questionnaire
                        if eq.question_id == question_id
                    ),
                    None,
                )

                question_dict = {
                    "question_id": question_id,
                    "content": question.content if question else None,
                    "answers": [],
                }
                # print("HERE7")
                for answer_id, answer_details in answers.items():
                    # Fetch answer details
                    answer = next(
                        (
                            eq.answer
                            for eq in entity_questionnaire
                            if eq.answer_id == answer_id
                        ),
                        None,
                    )

                    answer_dict = {
                        "answer_id": answer_id,
                        "content": answer.content if answer else None,
                        "details": answer_details,
                    }
                    question_dict["answers"].append(answer_dict)
                questionnaire_dict["questions"].append(question_dict)
            # print("HERE8")
            result.append(questionnaire_dict)

        return result


class EntityQuestionnaireBase(BaseSchema, EntityQuestionnaireMixin):
    entity_questionnaire_id: Optional[UUID] = None
    entity_id: UUID
    entity_type: EntityTypeEnum
    questionnaire_id: Optional[UUID] = None
    question_id: Optional[UUID] = None
    answer_id: Optional[UUID] = None
    mark_as_read: bool = False
    questionnaire: Optional[QuestionnaireBase] = None
    question: Optional[QuestionBase] = None
    asnwer: Optional[AnswerBase] = None

    @classmethod
    def model_validate(cls, entity_questionnaire: Union[EntityQuestionnaireModel]):
        # print("in model validate")
        return cls(
            entity_questionnaire_id=entity_questionnaire.entity_questionnaire_id,
            entity_id=entity_questionnaire.entity_id,
            entity_type=entity_questionnaire.entity_type,
            questionnaire_id=entity_questionnaire.questionnaire_id,
            question_id=entity_questionnaire.question_id,
            answer_id=entity_questionnaire.answer_id,
            mark_as_read=entity_questionnaire.mark_as_read,
            questionnaire=QuestionnaireBase.model_validate(
                entity_questionnaire.questionnaire
            )
            if entity_questionnaire.questionnaire
            else None,
            question=QuestionBase.model_validate(entity_questionnaire.question)
            if entity_questionnaire.question
            else None,
            answer=AnswerBase.model_validate(entity_questionnaire.answer)
            if entity_questionnaire.answer
            else None,
        ).model_dump()


class EntityQuestionnaire(EntityQuestionnaireBase):
    entity_questionnaire_id: Optional[UUID] = None
