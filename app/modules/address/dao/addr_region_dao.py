# dao
from app.modules.common.dao.base_dao import BaseDAO

# models
from app.modules.address.models.region import Region


class RegionDAO(BaseDAO[Region]):
    def __init__(self, excludes=[]):
        self.model = Region

        super().__init__(self.model, excludes=excludes)
