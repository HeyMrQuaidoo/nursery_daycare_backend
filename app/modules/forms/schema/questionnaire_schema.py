from uuid import UUID
from pydantic import ConfigDict
from typing import Optional

# models
from app.modules.forms.models.questionnaire import Questionnaire as QuestionnaireModel

# schemas
from app.modules.forms.schema.mixins.questionnaire_mixin import (
    QuestionnaireMixin,
    QuestionnaireBase,
)


class QuestionnaireResponse(QuestionnaireBase, QuestionnaireMixin):
    questionnaire_id: Optional[UUID] = None

    @classmethod
    def model_validate(cls, questionnaire: QuestionnaireModel):
        return cls.get_questionnaire_info(questionnaire)


class QuestionnaireCreateSchema(QuestionnaireBase):
    questionnaire_id: Optional[UUID] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": QuestionnaireMixin._questionnaire_create_json},
    )

    @classmethod
    def model_validate(cls, questionnaire: QuestionnaireModel):
        return cls.get_questionnaire_info(questionnaire)


class QuestionnaireUpdateSchema(QuestionnaireBase, QuestionnaireMixin):
    title: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": QuestionnaireMixin._questionnaire_update_json},
    )

    @classmethod
    def model_validate(cls, questionnaire: QuestionnaireModel):
        return cls.get_questionnaire_info(questionnaire)
