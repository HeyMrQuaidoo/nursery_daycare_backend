from typing import Dict, Any, List, Optional

# dao
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.forms.dao.answer_dao import AnswerDAO
# from app.modules.forms.dao.questionnaire_dao import QuestionnaireDAO

# models
from app.modules.forms.models.question import Question


class QuestionDAO(BaseDAO[Question]):
    def __init__(self, excludes: Optional[List[str]] = [""]):
        self.model = Question

        self.answer_dao = AnswerDAO()
        # self.questionnaire_dao = QuestionnaireDAO()

        self.detail_mappings: Dict[str, Any] = {
            # "questionnaire": self.questionnaire_dao,
            "answers": self.answer_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="question_id",
        )
