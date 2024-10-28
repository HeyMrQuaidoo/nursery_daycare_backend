from datetime import datetime
from uuid import UUID
from typing import Any, List, Optional, Union

# enum
from app.modules.forms.enums.questionnaire_enums import QuestionType

# base
from app.modules.forms.schema.question_schema import QuestionResponse
from app.modules.common.schema.base_schema import BaseSchema, BaseFaker
from app.modules.forms.schema.mixins.question_mixin import QuestionBase

# models
from app.modules.forms.models.questionnaire import Questionnaire as QuestionnaireModel


class QuestionnaireMixin:
    _title = BaseFaker.sentence()
    _description = BaseFaker.text(max_nb_chars=200)
    _content = BaseFaker.sentence()
    _question_answer_type = BaseFaker.random_element([e.value for e in QuestionType])
    _answer_content_1 = BaseFaker.sentence()
    _answer_content_2 = BaseFaker.sentence()

    _questionnaire_create_json = {
        "title": _title,
        "description": _description,
        "published": False,
        "publish_for_registration": False,
        "questions": [
            {
                "content": _content,
                "question_type": _question_answer_type,
                "answers": [
                    {
                        "content": _answer_content_1,
                        "answer_type": _question_answer_type,
                    },
                    {
                        "content": _answer_content_2,
                        "answer_type": _question_answer_type,
                    },
                ],
            }
        ],
    }

    _questionnaire_update_json = {
        "title": _title,
        "description": _description,
    }

    @classmethod
    def get_questionnaire_info(
        cls, questionnaire: Union[QuestionnaireModel, List[QuestionnaireModel], Any]
    ) -> List[QuestionnaireModel]:
        if not questionnaire:
            return []

        if isinstance(questionnaire, list):
            return [
                cls(
                    questionnaire_id=q.questionnaire_id,
                    title=q.title,
                    description=q.description,
                    published=questionnaire.published,
                    publish_for_registration=questionnaire.publish_for_registration,
                    created_at=questionnaire.created_at,
                    updated_at=questionnaire.updated_at,
                    number_of_responses=questionnaire.number_of_responses,
                    questions=[
                        QuestionResponse.model_validate(qs) for qs in q.questions
                    ],
                ).model_dump()
                for q in questionnaire
            ]

        return cls(
            questionnaire_id=questionnaire.questionnaire_id,
            title=questionnaire.title,
            description=questionnaire.description,
            published=questionnaire.published,
            publish_for_registration=questionnaire.publish_for_registration,
            created_at=questionnaire.created_at,
            updated_at=questionnaire.updated_at,
            number_of_responses=questionnaire.number_of_responses,
            questions=[
                QuestionResponse.model_validate(qs) for qs in questionnaire.questions
            ],
        ).model_dump()


class QuestionnaireBase(BaseSchema, QuestionnaireMixin):
    # questionnaire_id: Optional[UUID] = None
    title: str
    description: str
    questions: Optional[List[QuestionBase]] = None
    publish_for_registration: bool = False
    published: bool = False
    created_at: datetime = None
    updated_at: datetime = None
    number_of_responses: int = 0

    @classmethod
    def model_validate(cls, questionnaire: QuestionnaireModel):
        return cls.get_questionnaire_info(questionnaire)


class Questionnaire(QuestionnaireBase):
    questionnaire_id: Optional[UUID] = None
