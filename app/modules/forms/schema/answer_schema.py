from uuid import UUID
from typing import Any, Optional

from pydantic import ConfigDict

# enums
from app.modules.forms.enums.questionnaire_enums import AnswerType

# models
from app.modules.forms.models.answer import Answer as AnswerModel

# schemas
from app.modules.forms.schema.mixins.answer_mixin import AnswerMixin, AnswerBase


class AnswerResponse(AnswerBase, AnswerMixin):
    @classmethod
    def model_validate(cls, answer: AnswerModel):
        return cls.get_answer_info(answer)


class AnswerCreateSchema(AnswerBase, AnswerMixin):
    questionnaire_id: Optional[UUID] = None
    mark_as_read: Optional[bool] = False

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": AnswerMixin._answer_create_json},
    )

    @classmethod
    def model_validate(cls, answer: AnswerModel):
        return cls.get_answer_info(answer)


class AnswerUpdateSchema(AnswerBase, AnswerMixin):
    question_id: UUID = None
    answer_type: AnswerType = None
    content: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": AnswerMixin._answer_update_json},
    )

    @classmethod
    def model_validate(cls, answer: AnswerModel):
        return cls.get_answer_info(answer)
