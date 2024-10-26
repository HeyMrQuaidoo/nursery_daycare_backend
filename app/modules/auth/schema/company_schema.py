from pydantic import UUID4

from app.modules.common.schema.base_schema import BaseSchema


class CompanyBase(BaseSchema):
    company_name: str
    company_website: str


class Company(CompanyBase):
    company_id: UUID4
