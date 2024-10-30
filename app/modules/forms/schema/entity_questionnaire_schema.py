from uuid import UUID
from typing import Optional, Union
from pydantic import ConfigDict
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum
from app.modules.forms.schema.mixins.entity_questionnaire_mixin import (
    EntityQuestionnaireBase,
    EntityQuestionnaireMixin,
)


class EntityQuestionnaireResponse(EntityQuestionnaireBase, EntityQuestionnaireMixin):
    entity_questionnaire_id: Optional[UUID] = None
    entity_id: UUID
    entity_type: EntityTypeEnum
    questionnaire_id: Optional[UUID] = None
    question_id: Optional[UUID] = None
    answer_id: Optional[UUID] = None
    mark_as_read: bool = False

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": EntityQuestionnaireMixin._entity_questionnaire_create_json
        },
    )

    @classmethod
    def model_validate(cls, entity_questionnaire: Union[EntityQuestionnaireBase]):
        print(f"TYPE: {type(entity_questionnaire)}")
        return cls.get_entity_questionnaire_info(entity_questionnaire)


class EntityQuestionnaireCreateSchema(EntityQuestionnaireBase):
    entity_id: UUID
    entity_type: EntityTypeEnum
    questionnaire_id: Optional[UUID] = None
    question_id: Optional[UUID] = None
    answer_id: Optional[UUID] = None
    mark_as_read: bool = False

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": EntityQuestionnaireMixin._entity_questionnaire_create_json
        },
    )


class EntityQuestionnaireUpdateSchema(EntityQuestionnaireBase):
    mark_as_read: Optional[bool] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": EntityQuestionnaireMixin._entity_questionnaire_update_json
        },
    )
