from typing import List

# DAO
from app.modules.forms.dao.questionnaire_dao import QuestionnaireDAO

# Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import QuestionnaireSchema
from app.modules.forms.schema.questionnaire_schema import (
    QuestionnaireCreateSchema,
    QuestionnaireUpdateSchema,
)


class QuestionnaireRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        QuestionnaireSchema["create_schema"] = QuestionnaireCreateSchema
        QuestionnaireSchema["update_schema"] = QuestionnaireUpdateSchema
        self.dao: QuestionnaireDAO = QuestionnaireDAO(
            excludes=["entity_questionnaires"]
        )

        super().__init__(
            dao=self.dao, schemas=QuestionnaireSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        pass
