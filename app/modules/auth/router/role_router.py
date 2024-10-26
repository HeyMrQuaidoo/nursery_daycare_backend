from typing import List

# dao
from app.modules.auth.dao.role_dao import RoleDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import RoleSchema
from app.modules.auth.schema.role_schema import RoleUpdateSchema, RoleCreateSchema


class RoleRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        RoleSchema["create_schema"] = RoleCreateSchema
        RoleSchema["update_schema"] = RoleUpdateSchema
        self.dao: RoleDAO = RoleDAO(excludes=["users"])

        super().__init__(dao=self.dao, schemas=RoleSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
