import uuid
from importlib import import_module
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates, Session
from sqlalchemy import UUID, ForeignKey, Enum, Boolean, CheckConstraint, event, inspect

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
        ForeignKey("questionnaires.questionnaire_id", ondelete="CASCADE"),
        nullable=True,
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("questions.question_id", ondelete="CASCADE"),
        nullable=True,
    )
    answer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("answers.answer_id", ondelete="CASCADE"),
        nullable=True,
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
        "Questionnaire",
        back_populates="entity_questionnaires",
        lazy="selectin",
        viewonly=True,
    )

    # question
    question: Mapped["Question"] = relationship(
        "Question", lazy="selectin", viewonly=True
    )

    # answer
    answer: Mapped["Answer"] = relationship("Answer", lazy="selectin", viewonly=True)

    # user
    user: Mapped["User"] = relationship(
        "User",
        back_populates="entity_questionnaires",
        lazy="selectin",
        foreign_keys="User.user_id",
        viewonly=True,
        primaryjoin="and_(User.user_id==EntityQuestionnaire.entity_id)",
    )

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


@event.listens_for(EntityQuestionnaire, "after_insert")
def increment_number_of_responses(mapper, connection, target):
    state = inspect(target)

    if state.attrs.questionnaire_id.history.has_changes():
        # Only update if the entity_type is "user"
        if target.entity_type == EntityTypeEnum.user.name:
            models_module = import_module("app.modules.forms.models.questionnaire")
            questionnaire_model = getattr(models_module, "Questionnaire")

            # Access the session to update the Questionnaire model
            session = Session(connection)

            if session is not None:
                # Find the Questionnaire record and increment number_of_responses
                questionnaire = (
                    session.query(questionnaire_model)
                    .filter(
                        questionnaire_model.questionnaire_id == target.questionnaire_id
                    )
                    .one_or_none()
                )

                if questionnaire:
                    # questionnaire.number_of_responses = (
                    #     questionnaire.number_of_responses + 1
                    # )
                    # Count the distinct `entity_id`s with `entity_type` = "user" for this questionnaire
                    distinct_user_count = (
                        session.query(EntityQuestionnaire.entity_id)
                        .filter(
                            EntityQuestionnaire.entity_type == EntityTypeEnum.user,
                            EntityQuestionnaire.questionnaire_id
                            == target.questionnaire_id,
                        )
                        .distinct()
                        .count()
                    )
                    questionnaire.number_of_responses = distinct_user_count
                    session.add(questionnaire)
                    session.commit()  # Save the updated number_of_responses
                session.close()
