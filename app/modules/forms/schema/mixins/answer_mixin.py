from uuid import UUID
from typing import Any, List, Optional, Union

# schemas
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema

# enums
from app.modules.forms.enums.questionnaire_enums import AnswerType

# models
from app.modules.forms.models.answer import Answer as AnswerModel


class AnswerMixin:
    _answer_type = BaseFaker.random_element([e.value for e in AnswerType])
    _content = BaseFaker.sentence()

    _answer_create_json = {
        # "question_id": str(
        #     UUID(int=1)
        # ),  # Replace with realistic UUID example if available
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
                    answer_type=a.answer_type,
                    content=a.content,
                ).model_dump()
                for a in answer
            ]

        return cls(
            answer_id=answer.answer_id,
            question_id=answer.question_id,
            answer_type=answer.answer_type,
            content=answer.content,
        ).model_dump()


class AnswerBase(BaseSchema, AnswerMixin):
    answer_id: Optional[UUID] = None
    question_id: Optional[UUID] = None
    answer_type: AnswerType
    content: Optional[str] = None

    @classmethod
    def model_validate(cls, answer: AnswerModel):
        return cls.get_answer_info(answer)


class Answer(AnswerBase):
    answer_id: Optional[UUID] = None
