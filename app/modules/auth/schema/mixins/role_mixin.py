from pydantic import UUID4
from typing import List, Optional, Union

# models

# schema
from app.modules.auth.schema.permission import Permission
from app.modules.common.schema.base_schema import BaseSchema


class RoleBase(BaseSchema):
    name: str
    alias: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[Union[List[Permission]]] = []


class Role(RoleBase):
    role_id: UUID4
