from typing import List

# dao
from app.modules.resources.dao.media_dao import MediaDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import MediaSchema
from app.modules.resources.schema.media_schema import (
    MediaCreateSchema,
    MediaUpdateSchema,
)


class MediaRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        MediaSchema["create_schema"] = MediaCreateSchema
        MediaSchema["update_schema"] = MediaUpdateSchema
        self.dao: MediaDAO = MediaDAO(excludes=[])

        super().__init__(dao=self.dao, schemas=MediaSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
