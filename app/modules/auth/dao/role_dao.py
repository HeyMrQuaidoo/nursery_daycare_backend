from sqlalchemy.sql import func
from sqlalchemy.future import select
from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

# core

# models
from app.modules.auth.models.role import Role

# dao
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.address.dao.address_dao import AddressDAO
from app.modules.auth.dao.permission_dao import PermissionDAO

# schemas


class RoleDAO(BaseDAO[Role]):
    def __init__(self, excludes: Optional[List[str]] = []):
        self.model = Role

        self.address_dao = AddressDAO()
        self.permission_dao = PermissionDAO()
        self.detail_mappings = {
            "permissions": self.permission_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="role_id",
        )

    async def _fetch_role_stats(self, db_session: AsyncSession) -> Dict[str, int]:
        """
        Fetch statistics for roles, such as the number of users associated with each role.
        """
        async with db_session as db:
            stmt = select(
                Role.name, func.count(Role.name).label("user_count")
            ).group_by(Role.name)
            query_result = await db.execute(stmt)
            role_stats_results = query_result.all()

        return {name: count for name, count in role_stats_results}
