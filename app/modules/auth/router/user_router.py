from typing import List

# dao
from app.modules.auth.dao.user_dao import UserDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import UserSchema
from app.modules.auth.schema.user_schema import UserCreateSchema


class UserRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: UserDAO = UserDAO(excludes=[""])
        UserSchema["create_schema"] = UserCreateSchema
        UserSchema["update_schema"] = UserCreateSchema

        super().__init__(dao=self.dao, schemas=UserSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
