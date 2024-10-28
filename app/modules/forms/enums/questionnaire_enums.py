import enum


class AnswerType(enum.Enum):
    text = "text"
    short_text = "short_text"
    long_text = "long_text"
    multichoice = "multichoice"
    checkbox = "checkbox"


class QuestionType(enum.Enum):
    text = "text"
    short_text = "short_text"
    long_text = "long_text"
    multichoice = "multichoice"
    checkbox = "checkbox"


class EntityType(enum.Enum):
    question = "question"
    user = "user"
