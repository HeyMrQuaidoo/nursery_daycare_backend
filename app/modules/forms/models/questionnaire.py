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

    # Relationships
    questions: Mapped[List["Question"]] = relationship(
        "Question",
        back_populates="questionnaire",
        cascade="all, delete-orphan",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )
    entity_questionnaires = relationship(
        "EntityQuestionnaire",
        back_populates="questionnaire",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # questions: Mapped[List["Question"]] = relationship(
    #     "Question",
    #     secondary="entity_questionnaires",
    #     primaryjoin="and_(Questionnaire.questionnaire_id==EntityQuestionnaire.entity_id, EntityQuestionnaire.entity_type=='questions')",
    #     back_populates="questionnaire",
    #     cascade="all, delete-orphan",
    #     lazy="selectin",
    #     viewonly=True,
    #     collection_class=BaseModelCollection,
    # )


# register model
Base.setup_model_dynamic_listener("questionnaires", Questionnaire)
