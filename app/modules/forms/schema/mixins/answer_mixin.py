from uuid import UUID
from typing import Any, List, Optional, Union

# schemas
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema

# enums
from app.modules.forms.enums.questionnaire_enums import AnswerType

# models
from app.modules.forms.models.answer import Answer as AnswerModel
from app.modules.forms.models.question import Question as QuestionModel

class AnswerMixin:
    _answer_type = BaseFaker.random_element([e.value for e in AnswerType])
    _content = BaseFaker.sentence()

    _answer_create_json = {
        "answer_type": _answer_type[0],
        "content": _content,
    }

    _answer_update_json = {
        "answer_type": _answer_type[0],
        "content": _content,
    }

    @classmethod
    def get_answer_info(
        cls, answer: Union[AnswerModel, List[AnswerModel], Any]
    ) -> list[AnswerModel]:
        if not answer:
            return []

        if isinstance(answer, list):
            return [
                cls(
                    answer_id=a.answer_id,
                    question_id=a.question_id,
                    questionnaire_id=a.question.questionnaire_id
                    if isinstance(a.question, QuestionModel)
                    else None,
                    answer_type=a.answer_type,
                    content=a.content,
                ).model_dump(exclude=["mark_as_read"])
                for a in answer
            ]

        return cls(
            answer_id=answer.answer_id,
            question_id=answer.question_id,
            questionnaire_id=answer.question.questionnaire_id
            if isinstance(answer.question, QuestionModel)
            else None,
            answer_type=answer.answer_type,
            content=answer.content,
        ).model_dump(exclude=["mark_as_read"])


class AnswerBase(BaseSchema, AnswerMixin):
    answer_id: Optional[UUID] = None
    questionnaire_id: Optional[UUID] = None
    question_id: Optional[UUID] = None
    answer_type: AnswerType
    content: Optional[str] = None
    mark_as_read: Optional[bool] = False

    @classmethod
    def model_validate(cls, answer: AnswerModel):
        return cls.get_answer_info(answer)


class Answer(AnswerBase):
    answer_id: Optional[UUID] = None
