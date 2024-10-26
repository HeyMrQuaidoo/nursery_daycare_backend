# dao
from typing import List, Optional

# from app.modules.auth.dao.role_dao import RoleDAO
from app.modules.common.dao.base_dao import BaseDAO

# models
from app.modules.auth.models.permissions import Permissions


class PermissionDAO(BaseDAO[Permissions]):
    def __init__(self, excludes: Optional[List[str]] = []):
        self.model = Permissions

        # self.role_dao = RoleDAO()

        self.detail_mappings = {
            # "roles": self.role_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="permission_id",
        )
