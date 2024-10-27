from uuid import UUID
from collections import defaultdict
from typing import Any, List, Optional, Union

# schema
from app.modules.common.schema.base_schema import BaseSchema, BaseFaker

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
            EntityQuestionnaireModel,
            Union[List[EntityQuestionnaireModel] | EntityQuestionnaireModel | Any],
        ],
    ) -> List[dict]:
        if not entity_questionnaire:
            return []

        if not isinstance(entity_questionnaire, list):
            entity_questionnaire = [entity_questionnaire]

        # nested dictionary structure
        data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

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

        result = []
        for questionnaire_id, questions in data.items():
            # Fetch questionnaire details
            questionnaire = next(
                (
                    eq.questionnaire
                    for eq in entity_questionnaire
                    if eq.questionnaire_id == questionnaire_id
                ),
                None,
            )

            questionnaire_dict = {
                "questionnaire_id": questionnaire_id,
                "title": questionnaire.title if questionnaire else None,
                "description": questionnaire.description if questionnaire else None,
                "questions": [],
            }
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
            result.append(questionnaire_dict)

        return result


class EntityQuestionnaireBase(BaseSchema, EntityQuestionnaireMixin):
    # entity_questionnaire_id: Optional[UUID] = None
    entity_id: UUID
    entity_type: EntityTypeEnum
    questionnaire_id: Optional[UUID] = None
    question_id: Optional[UUID] = None
    answer_id: Optional[UUID] = None
    mark_as_read: bool = False


class EntityQuestionnaire(EntityQuestionnaireBase):
    entity_questionnaire_id: Optional[UUID] = None
