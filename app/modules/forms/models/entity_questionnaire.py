import uuid
from sqlalchemy import UUID, ForeignKey, Enum, Boolean, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates

from app.modules.associations.enums.entity_type_enums import EntityTypeEnum

# models
from app.modules.common.models.model_base import BaseModel as Base


class EntityQuestionnaire(Base):
    __tablename__ = "entity_questionnaires"

    entity_questionnaire_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    entity_type: Mapped["EntityTypeEnum"] = mapped_column(Enum(EntityTypeEnum))
    questionnaire_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("questionnaires.questionnaire_id"),
        nullable=True,
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("questions.question_id"), nullable=True
    )
    answer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("answers.answer_id"), nullable=True
    )
    mark_as_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('user', 'questions', 'questionnaires', 'answers')",
            name="check_entity_type_address",
        ),
    )

    __mapper_args__ = {"eager_defaults": True}

    # questionnaire
    questionnaire: Mapped["Questionnaire"] = relationship(
        "Questionnaire", back_populates="entity_questionnaires", lazy="selectin"
    )

    # question
    question: Mapped["Question"] = relationship("Question", lazy="selectin")

    # answer
    answer: Mapped["Answer"] = relationship("Answer", lazy="selectin")

    @validates("entity_type", "entity_id")
    def validate_entity(self, key, value, **kwargs):
        if key == "entity_id":
            entity_id = value
            entity_type = kwargs.get("entity_type", self.entity_type)
        elif key == "entity_type":
            entity_type = value
            entity_id = self.entity_id

        entity_map = {
            EntityTypeEnum.user: ("users", "user_id"),
            EntityTypeEnum.questionnaires: ("questionnaires", "questionnaire_id"),
            EntityTypeEnum.questions: ("questions", "question_id"),
            EntityTypeEnum.answers: ("answers", "answer_id"),
        }

        if entity_type and EntityTypeEnum(str(entity_type)) in entity_map:
            super().validate_entity(
                entity_id=entity_id,
                entity_type=EntityTypeEnum(str(entity_type)),
                entity_map=entity_map,
            )
        return value
