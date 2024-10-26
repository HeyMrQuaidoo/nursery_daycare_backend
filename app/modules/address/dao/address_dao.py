from typing import Any, Dict
from typing_extensions import override
from sqlalchemy.ext.asyncio import AsyncSession

# models
from app.modules.address.models.city import City
from app.modules.address.models.region import Region
from app.modules.address.models.country import Country
from app.modules.address.models.address import Addresses as AddressModel

# daos
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.address.dao.addr_city_dao import CityDAO
from app.modules.address.dao.addr_region_dao import RegionDAO
from app.modules.address.dao.addr_country_dao import CountryDAO
from app.modules.address.dao.entity_address_dao import EntityAddressDAO

# schemas
from app.modules.address.schema.address_schema import AddressCreateSchema

# enums
from app.modules.address.enums.address_enums import AddressTypeEnum


class AddressDAO(BaseDAO[AddressModel]):
    def __init__(self, excludes=[]):
        self.detail_mappings = {}

        self.model = AddressModel
        self.city_dao = CityDAO()
        self.region_dao = RegionDAO()
        self.country_dao = CountryDAO()
        self.entity_address_dao = EntityAddressDAO()

        super().__init__(self.model, excludes=excludes, primary_key="address_id")

    async def get_location_info(
        self, db_session: AsyncSession, address_data: AddressCreateSchema
    ) -> AddressCreateSchema:
        try:
            country: Country = await self.country_dao.query_on_create(
                db_session=db_session,
                filters={"country_name": address_data.country},
                single=True,
                create_if_not_exist=True,
            )
            region: Region = await self.region_dao.query_on_create(
                db_session=db_session,
                filters={
                    "country_id": country.country_id,
                    "region_name": address_data.region,
                },
                single=True,
                create_if_not_exist=True,
            )
            city: City = await self.city_dao.query_on_create(
                db_session=db_session,
                filters={"region_id": region.region_id, "city_name": address_data.city},
                single=True,
                create_if_not_exist=True,
            )

            # set address data
            address_data.city = city
            address_data.region = region
            address_data.country = country
            address_data.address_type = AddressTypeEnum(address_data.address_type)

        except Exception as e:
            raise Exception(str(e))

        return address_data

    @override
    async def create(self, db_session: AsyncSession, obj_in: AddressCreateSchema):
        address_data = await self.get_location_info(
            db_session=db_session, address_data=AddressCreateSchema(**obj_in)
        )

        result = await super().create(
            db_session=db_session,
            obj_in={
                **address_data.model_dump(),
                "city_id": str(address_data.city.city_id),
                "country_id": str(address_data.country.country_id),
                "region_id": str(address_data.region.region_id),
            },
        )

        return result if result else None

    @override
    async def update(
        self, db_session: AsyncSession, db_obj: AddressModel, obj_in: Dict[str, Any]
    ):
        address_data = AddressCreateSchema(**obj_in)
        address_data = await self.get_location_info(db_session, address_data)

        result = await super().update(
            db_session=db_session, db_obj=db_obj, obj_in=address_data
        )

        return result if result else None
