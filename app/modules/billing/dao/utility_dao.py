from typing import Optional, List

# daos
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.resources.dao.media_dao import MediaDAO

# models
from app.modules.billing.models.utility import Utilities


class UtilityDAO(BaseDAO[Utilities]):
    def __init__(self, excludes: Optional[List[str]] = []):
        self.model = Utilities

        self.media_dao = MediaDAO()
        self.detail_mappings = {"media": self.media_dao}

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="utility_id",
        )
