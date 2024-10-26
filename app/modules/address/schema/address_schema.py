from uuid import UUID, uuid4
from typing import Annotated, Any, Optional, Union
from pydantic import BaseModel, constr, ConfigDict, field_validator

# enums
from app.modules.address.enums.address_enums import AddressTypeEnum

# models
from app.modules.address.models.city import City as CityModel
from app.modules.address.models.region import Region as RegionModel
from app.modules.address.models.country import Country as CountryModel


class City(BaseModel):
    city_id: Annotated[UUID, uuid4()] = uuid4()
    region_id: UUID
    city_name: Annotated[str, constr(max_length=128)]

    model_config = ConfigDict(
        __allow_unmapped__=True, from_attributes=True, use_enum_values=True
    )


class Region(BaseModel):
    region_id: Annotated[UUID, uuid4()] = uuid4()
    country_id: UUID
    region_name: Annotated[str, constr(max_length=128)]

    model_config = ConfigDict(
        __allow_unmapped__=True, from_attributes=True, use_enum_values=True
    )


class Country(BaseModel):
    country_id: Annotated[UUID, uuid4()] = uuid4()
    country_name: Annotated[str, constr(max_length=128)]

    model_config = ConfigDict(
        __allow_unmapped__=True, from_attributes=True, use_enum_values=True
    )


class AddressBase(BaseModel):
    address_id: Optional[UUID] = None
    address_type: AddressTypeEnum
    primary: Optional[bool] = True
    address_1: Optional[str]
    address_2: Optional[str] = None
    city: Union[str, UUID, City, Any]
    region: Union[str, UUID, Region, Any]
    country: Union[str, UUID, Country, Any]
    address_postalcode: Optional[str]
    emergency_address: bool = False
    # emergency_address_hash: Optional[str] = "bf455a82-b529-4ab8-a451-70c8763591da"

    model_config = ConfigDict(
        __allow_unmapped__=True,
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "address_type": "billing",
                "primary": True,
                "address_1": "line 1",
                "address_2": "line 2",
                "city": "Tema",
                "region": "Greater Accra",
                "country": "Ghana",
                "address_postalcode": "",
            }
        },
    )


class EmergencyAddressBase(AddressBase):
    emergency_address: bool = True

    model_config = ConfigDict(
        __allow_unmapped__=True,
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "address_type": "billing",
                "primary": True,
                "address_1": "line 1",
                "address_2": "line 2",
                "city": "Tema",
                "region": "Greater Accra",
                "country": "Ghana",
                "address_postalcode": "",
            }
        },
    )


class AddressCreateSchema(AddressBase):
    model_config = ConfigDict(
        __allow_unmapped__=True,
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "address_type": "billing",
                "primary": True,
                "address_1": "line 1",
                "address_2": "line 2",
                "city": "Tema",
                "region": "Greater Accra",
                "country": "Ghana",
                "address_postalcode": "",
            }
        },
    )

    @field_validator("city", mode="before")
    def validate_city(cls, value):
        if isinstance(value, CityModel):
            return City.model_validate(value).city_name
        elif isinstance(value, (str, UUID)):
            return value
        elif isinstance(value, dict):
            return City(**value).city_name
        raise ValueError("Invalid city value")

    @field_validator("region", mode="before")
    def validate_region(cls, value):
        if isinstance(value, RegionModel):
            return Region.model_validate(value).region_name
        elif isinstance(value, (str, UUID)):
            return value
        elif isinstance(value, dict):
            return Region(**value).region_name
        raise ValueError("Invalid region value")

    @field_validator("country", mode="before")
    def validate_country(cls, value):
        if isinstance(value, CountryModel):
            return Country.model_validate(value).country_name
        elif isinstance(value, (str, UUID)):
            return value
        elif isinstance(value, dict):
            return Country(**value).country_name
        raise ValueError("Invalid country value")
