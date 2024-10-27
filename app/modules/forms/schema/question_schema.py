from uuid import UUID
from pydantic import ConfigDict
from typing import Optional

# enums
from app.modules.forms.enums.questionnaire_enums import QuestionType

# models
from app.modules.forms.models.question import Question as QuestionModel

# schemas
from app.modules.forms.schema.mixins.question_mixin import QuestionMixin, QuestionBase


class QuestionResponse(QuestionBase, QuestionMixin):
    @classmethod
    def model_validate(cls, question: QuestionModel):
        return cls.get_question_info(question)


class QuestionCreateSchema(QuestionBase, QuestionMixin):
    questionnaire_id: Optional[UUID] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": QuestionMixin._question_create_json},
    )

    @classmethod
    def model_validate(cls, question: QuestionModel):
        return cls.get_question_info(question)


class QuestionUpdateSchema(QuestionBase, QuestionMixin):
    content: Optional[str] = None
    question_type: Optional[QuestionType] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": QuestionMixin._question_update_json},
    )

    @classmethod
    def model_validate(cls, question: QuestionModel):
        return cls.get_question_info(question)
