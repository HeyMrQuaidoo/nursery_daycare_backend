from typing import List

# DAO
from app.modules.forms.dao.question_dao import QuestionDAO

# Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import QuestionSchema
from app.modules.forms.schema.question_schema import (
    QuestionCreateSchema,
    QuestionUpdateSchema,
)


class QuestionRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        QuestionSchema["create_schema"] = QuestionCreateSchema
        QuestionSchema["update_schema"] = QuestionUpdateSchema
        self.dao: QuestionDAO = QuestionDAO(excludes=[])

        super().__init__(dao=self.dao, schemas=QuestionSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
