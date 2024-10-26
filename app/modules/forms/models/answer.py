import uuid
from sqlalchemy import UUID, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

# enums
from app.modules.forms.enums.questionnaire_enums import AnswerType

# models
from app.modules.common.models.model_base import BaseModel as Base


class Answer(Base):
    __tablename__ = "answers"

    answer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("questions.question_id"), nullable=False
    )
    # respondent_id = Column(Integer, nullable=False)
    answer_type: Mapped["AnswerType"] = mapped_column(Enum(AnswerType), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)

    # question
    question: Mapped["Question"] = relationship(
        "Question", back_populates="answers", lazy="selectin"
    )


# register model
Base.setup_model_dynamic_listener("answers", Answer)
