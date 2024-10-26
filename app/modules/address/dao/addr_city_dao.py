# models
from app.modules.address.models.city import City

# dao
from app.modules.common.dao.base_dao import BaseDAO


class CityDAO(BaseDAO[City]):
    def __init__(self, excludes=[]):
        self.model = City

        super().__init__(model=self.model, excludes=excludes)
