import uuid
from typing import List
from sqlalchemy import UUID, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column


# enums
from app.modules.forms.enums.questionnaire_enums import QuestionType

# models
from app.modules.common.models.model_base import BaseModel as Base, BaseModelCollection


class Question(Base):
    __tablename__ = "questions"

    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    questionnaire_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("questionnaires.questionnaire_id"),
        nullable=True,
    )
    content: Mapped[str] = mapped_column(Text)
    question_type: Mapped["QuestionType"] = mapped_column(Enum(QuestionType))

    # questionnaire
    questionnaire: Mapped["Questionnaire"] = relationship(
        "Questionnaire", back_populates="questions", lazy="selectin"
    )

    # answers
    # answers: Mapped[List["Answer"]] = relationship(
    #     "Answer", back_populates="question", cascade="all, delete-orphan", lazy="selectin"
    # )

    answers: Mapped[List["Answer"]] = relationship(
        "Answer",
        secondary="entity_questionnaires",
        primaryjoin="and_(Question.question_id==EntityQuestionnaire.entity_id, EntityQuestionnaire.entity_type=='questions')",
        # secondaryjoin="and_(EntityAddress.address_id==Addresses.address_id, EntityAddress.emergency_address==False)",
        # back_populates="questionnaire",
        cascade="all, delete-orphan",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )


# register model
Base.setup_model_dynamic_listener("questions", Question)
