from typing import Any, Dict, List, Optional

# models
from app.modules.forms.models.answer import Answer

# dao
from app.modules.common.dao.base_dao import BaseDAO


class AnswerDAO(BaseDAO[Answer]):
    def __init__(self, excludes: Optional[List[str]] = [""]):
        self.model = Answer
        self.detail_mappings: Dict[str, Any] = {}

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="answer_id",
        )
