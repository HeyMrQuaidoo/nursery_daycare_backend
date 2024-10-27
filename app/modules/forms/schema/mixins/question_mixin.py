from uuid import UUID
from typing import Any, List, Optional, Union

# schema
from app.modules.forms.schema.answer_schema import AnswerResponse
from app.modules.forms.schema.mixins.answer_mixin import AnswerBase
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema

# enums
from app.modules.forms.enums.questionnaire_enums import QuestionType

# models
from app.modules.forms.models.question import Question as QuestionModel


class QuestionMixin(BaseSchema):
    _content = BaseFaker.sentence()
    # _question_type = BaseFaker.random_choices(["text", "multiple_choice", "boolean"], length=1)
    _question_type = BaseFaker.random_element([e.value for e in QuestionType])

    _question_create_json = {
        "questionnaire_id": str(
            UUID(int=1)
        ),  # Replace with realistic UUID example if available
        "content": _content,
        "question_type": _question_type[0],
    }

    _question_update_json = {
        "content": _content,
        "question_type": _question_type[0],
    }

    @classmethod
    def get_question_info(
        cls, question: Union[QuestionModel, List[QuestionModel], Any]
    ) -> List[QuestionModel]:
        if not question:
            return []

        if isinstance(question, list):
            return [
                cls(
                    question_id=q.question_id,
                    questionnaire_id=q.questionnaire_id,
                    content=q.content,
                    question_type=q.question_type,
                    answers=[AnswerResponse.model_validate(a) for a in q.answers],
                ).model_dump()
                for q in question
            ]

        return cls(
            question_id=question.question_id,
            questionnaire_id=question.questionnaire_id,
            content=question.content,
            question_type=question.question_type,
            answers=[AnswerResponse.model_validate(a) for a in question.answers],
        ).model_dump()


class QuestionBase(QuestionMixin):
    question_id: Optional[UUID] = None
    questionnaire_id: Optional[UUID] = None
    content: str
    question_type: QuestionType
    answers: Optional[List[AnswerBase]] = []

    @classmethod
    def model_validate(cls, question: QuestionModel):
        return cls.get_question_info(question)


class Question(QuestionBase):
    question_id: Optional[UUID] = None
