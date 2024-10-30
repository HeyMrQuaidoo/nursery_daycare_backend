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
        UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4
    )
    questionnaire_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("questionnaires.questionnaire_id"),
        nullable=True,
    )
    content: Mapped[str] = mapped_column(Text)
    question_type: Mapped["QuestionType"] = mapped_column(Enum(QuestionType))

    # entity_questionnaires
    entity_questionnaires: Mapped[List["EntityQuestionnaire"]] = relationship(
        "EntityQuestionnaire",
        back_populates="question",
        cascade="all, delete-orphan",
        lazy="selectin",
        uselist=True
    )

    # questionnaire
    questionnaire: Mapped["Questionnaire"] = relationship(
        "Questionnaire",
        back_populates="questions",
        lazy="selectin",
        single_parent=True,
    )

    # answers
    # answers = relationship(
    #     "Answer",
    #     back_populates="question",
    #     cascade="all, delete-orphan",
    #     lazy="selectin",
    # )
    answers: Mapped[List["Answer"]] = relationship(
        "Answer",
        secondary="entity_questionnaires",
        primaryjoin="and_(Question.question_id==EntityQuestionnaire.entity_id, Question.question_id==EntityQuestionnaire.question_id, EntityQuestionnaire.entity_type=='questions')",
        secondaryjoin="and_(EntityQuestionnaire.answer_id==Answer.answer_id)",
        back_populates="question",
        cascade="all, delete",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )


# register model
Base.setup_model_dynamic_listener("questions", Question)
