from pydantic import constr
from uuid import UUID, uuid4
from typing import Annotated, Any, Optional, List

# schemas
from app.modules.common.schema.base_schema import BaseSchema

# enums
from app.modules.address.enums.address_enums import AddressTypeEnum

# models
from app.modules.address.models.address import Addresses as AddressModel


class City(BaseSchema):
    """
    Model for representing a city.

    Attributes:
        city_id (UUID): The unique identifier for the city, defaults to a new UUID.
        region_id (UUID): The unique identifier for the associated region.
        city_name (str): The name of the city, with a maximum length of 128 characters.
    """

    city_id: Annotated[UUID, uuid4()] = uuid4()
    region_id: UUID
    city_name: Annotated[str, constr(max_length=128)]


class Region(BaseSchema):
    """
    Model for representing a region.

    Attributes:
        region_id (UUID): The unique identifier for the region, defaults to a new UUID.
        country_id (UUID): The unique identifier for the associated country.
        region_name (str): The name of the region, with a maximum length of 128 characters.
    """

    region_id: Annotated[UUID, uuid4()] = uuid4()
    country_id: UUID
    region_name: Annotated[str, constr(max_length=128)]


class Country(BaseSchema):
    """
    Model for representing a country.

    Attributes:
        country_id (UUID): The unique identifier for the country, defaults to a new UUID.
        country_name (str): The name of the country, with a maximum length of 128 characters.
    """

    country_id: Annotated[UUID, uuid4()] = uuid4()
    country_name: Annotated[str, constr(max_length=128)]


# Ensure pydantic schema is initialized TODO: Remove
City.model_rebuild()
Region.model_rebuild()
Country.model_rebuild()


class AddressBase(BaseSchema):
    """
    Base model for representing an address.

    Attributes:
        address_type (AddressTypeEnum): The type of the address.
        primary (Optional[bool]): Indicates if this is the primary address, defaults to True.
        address_1 (Optional[str]): The first line of the address.
        address_2 (Optional[str]): The second line of the address, defaults to None.
        city (str|UUID|Any): The city name or identifier.
        region (str|UUID|Any): The region name or identifier.
        country (str|UUID|Any): The country name or identifier.
        address_postalcode (Optional[str]): The postal code of the address.
    """

    address_type: AddressTypeEnum
    primary: Optional[bool] = True
    address_1: Optional[str]
    address_2: Optional[str] = None
    city: str | UUID | Any
    region: str | UUID | Any
    country: str | UUID | Any
    address_postalcode: Optional[str]

    # model_config = ConfigDict(from_attributes=True)


class Address(AddressBase):
    """
    Model for representing an address with an optional address ID.

    Attributes:
        address_id (Optional[UUID]): The unique identifier for the address, defaults to None.
    """

    address_id: Optional[UUID] = None


class AddressMixin:
    @classmethod
    def get_address_base(
        cls, addresses: List[AddressModel], include_emergency=True
    ) -> List[Address]:
        result = []

        for addr in addresses:
            addr_city: City = addr.city
            addr_region: Region = addr.region
            addr_country: Country = addr.country

            result.append(
                Address(
                    address_id=addr.address_id,
                    address_type=addr.address_type,
                    primary=addr.primary,
                    address_1=addr.address_1,
                    address_2=addr.address_2,
                    address_postalcode=addr.address_postalcode,
                    city=addr_city.city_name,
                    region=addr_region.region_name,
                    country=addr_country.country_name,
                )
            )

        return result
