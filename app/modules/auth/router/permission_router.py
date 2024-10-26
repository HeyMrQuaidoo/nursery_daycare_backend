from typing import List

# dao
from app.modules.auth.dao.permission_dao import PermissionDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import PermissionSchema
from app.modules.auth.schema.permission import (
    PermissionCreateSchema,
    PermissionUpdateSchema,
)


class PermissionRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        PermissionSchema["create_schema"] = PermissionCreateSchema
        PermissionSchema["update_schema"] = PermissionUpdateSchema
        self.dao: PermissionDAO = PermissionDAO(excludes=[""])

        super().__init__(
            dao=self.dao, schemas=PermissionSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        pass
