from typing import Any, Dict, List, Optional

# models
from app.modules.forms.models.questionnaire import Questionnaire

# dao
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.forms.dao.question_dao import QuestionDAO


class QuestionnaireDAO(BaseDAO[Questionnaire]):
    def __init__(self, excludes: Optional[List[str]] = [""]):
        self.model = Questionnaire
        self.question_dao = QuestionDAO()

        self.detail_mappings: Dict[str, Any] = {
            "questions": self.question_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="questionnaire_id",
        )
