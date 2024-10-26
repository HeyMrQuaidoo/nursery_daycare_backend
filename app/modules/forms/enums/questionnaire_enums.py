import enum


class AnswerType(enum.Enum):
    text = "text"
    multichoice = "multichoice"
    checkbox = "checkbox"


class QuestionType(enum.Enum):
    text = "text"
    multichoice = "multichoice"
    checkbox = "checkbox"


class EntityType(enum.Enum):
    question = "question"
    user = "user"
