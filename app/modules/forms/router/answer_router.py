from typing import List

# DAO
from app.modules.forms.dao.answer_dao import AnswerDAO

# Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import AnswerSchema
from app.modules.forms.schema.answer_schema import (
    AnswerCreateSchema,
    AnswerUpdateSchema,
)


class AnswerRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        AnswerSchema["create_schema"] = AnswerCreateSchema
        AnswerSchema["update_schema"] = AnswerUpdateSchema
        self.dao: AnswerDAO = AnswerDAO(excludes=[])

        super().__init__(dao=self.dao, schemas=AnswerSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
