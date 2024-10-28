import uuid
from typing import List
from sqlalchemy import UUID, Boolean, Integer, Text, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base, BaseModelCollection


class Questionnaire(Base):
    __tablename__ = "questionnaires"

    questionnaire_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(Text)
    publish_for_registration: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=True
    )
    published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    number_of_responses: Mapped[int] = mapped_column(Integer, default=0, nullable=True)

    # entity_questionnaires
    entity_questionnaires: Mapped[List["EntityQuestionnaire"]] = relationship(
        "EntityQuestionnaire",
        back_populates="questionnaire",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # questions
    questionnaire_questions: Mapped[List["Question"]] = relationship(
        "Question",
        back_populates="questionnaire",
        cascade="all, delete",
        lazy="selectin",
    )
    questions: Mapped[List["Question"]] = relationship(
        "Question",
        back_populates="questionnaire",
        cascade="all, delete, delete-orphan",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )


# register model
Base.setup_model_dynamic_listener("questionnaires", Questionnaire)
