from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Query, Request

# dao
from app.modules.auth.dao.role_dao import RoleDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import RoleSchema
from app.modules.auth.schema.role_schema import RoleUpdateSchema, RoleCreateSchema

# core
from app.core.lifespan import get_db
from app.core.response import DAOResponse
from app.core.errors import CustomException, RecordNotFoundException, IntegrityError


class RoleRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        RoleSchema["create_schema"] = RoleCreateSchema
        RoleSchema["update_schema"] = RoleUpdateSchema
        self.dao: RoleDAO = RoleDAO(excludes=["users"])

        super().__init__(
            dao=self.dao,
            schemas=RoleSchema,
            prefix=prefix,
            tags=tags,
            route_overrides=["get_all"],
        )
        self.register_routes()

    def register_routes(self):
        @self.router.get("/")
        async def get_all(
            request: Request,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ) -> DAOResponse:
            try:
                items = await self.dao.get_all(
                    db_session=db_session, offset=offset, limit=limit
                )

                meta = await self.dao.build_pagination_meta(
                    request=request, limit=limit, offset=offset, db_session=db_session
                )

                role_stats = await self.dao._fetch_role_stats(db_session)

                if isinstance(items, DAOResponse):
                    if hasattr(items, "meta") and getattr(items, "meta"):
                        meta_data = items.meta
                        meta.update(meta_data)
                    items.set_meta(meta)

                return (
                    items
                    if isinstance(items, DAOResponse)
                    else DAOResponse(
                        success=True,
                        data=items,
                        meta={**meta, "role_stats": role_stats},
                    )
                )
            except RecordNotFoundException as e:
                raise e
            except IntegrityError as e:
                raise e
            except Exception as e:
                raise CustomException(e)
