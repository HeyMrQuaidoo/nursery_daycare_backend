from typing import List

# dao
from app.modules.billing.dao.utility_dao import UtilityDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import UtilitySchema
from app.modules.billing.schema.utility_schema import (
    UtilityCreateSchema,
    UtilityUpdateSchema,
)


class UtilityRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        UtilitySchema["create_schema"] = UtilityCreateSchema
        UtilitySchema["update_schema"] = UtilityUpdateSchema
        self.dao: UtilityDAO = UtilityDAO(excludes=[])

        super().__init__(dao=self.dao, schemas=UtilitySchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
