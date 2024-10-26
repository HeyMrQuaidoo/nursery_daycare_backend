from app.modules.common.dao.base_dao import BaseDAO


from app.modules.associations.models.entity_address import EntityAddress


class EntityAddressDAO(BaseDAO[EntityAddress]):
    def __init__(self, excludes=[]):
        self.model = EntityAddress

        super().__init__(self.model, excludes=excludes)
