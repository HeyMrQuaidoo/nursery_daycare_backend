import uuid
from sqlalchemy import UUID, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

# enums
from app.modules.forms.enums.questionnaire_enums import AnswerType

# models
from app.modules.common.models.model_base import BaseModel as Base, BaseModelCollection


class Answer(Base):
    __tablename__ = "answers"

    answer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("questions.question_id", ondelete="CASCADE"),
        nullable=False,
    )
    # respondent_id = Column(Integer, nullable=False)
    answer_type: Mapped["AnswerType"] = mapped_column(Enum(AnswerType), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)

    # entity_questionnaires
    entity_questionnaires = relationship(
        "EntityQuestionnaire", back_populates="answer", cascade="all, delete-orphan"
    )

    # question
    question = relationship(
        "Question",
        secondary="entity_questionnaires",
        back_populates="answers",
        lazy="selectin",
        cascade="all, delete",
        viewonly=True,
        collection_class=BaseModelCollection,
    )


# register model
Base.setup_model_dynamic_listener("answers", Answer)
