# models
from app.modules.address.models.country import Country

# dao
from app.modules.common.dao.base_dao import BaseDAO


class CountryDAO(BaseDAO[Country]):
    def __init__(self, excludes=[]):
        self.model = Country

        super().__init__(self.model, excludes=excludes)
