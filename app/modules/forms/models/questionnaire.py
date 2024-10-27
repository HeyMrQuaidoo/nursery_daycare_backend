import uuid
from typing import List
from sqlalchemy import UUID, Text, String
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

    # entity_questionnaires
    entity_questionnaires: Mapped[List["EntityQuestionnaire"]] = relationship(
        "EntityQuestionnaire",
        back_populates="questionnaire",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # questions
    questions: Mapped[List["Question"]] = relationship(
        "Question",
        back_populates="questionnaire",
        cascade="all, delete",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )


# register model
Base.setup_model_dynamic_listener("questionnaires", Questionnaire)
