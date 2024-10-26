from typing import List, Optional

# Models
from app.modules.resources.models.media import Media

# Base DAO
from app.modules.common.dao.base_dao import BaseDAO


class MediaDAO(BaseDAO[Media]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Media
        self.detail_mappings = {}
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="media_id",
        )
