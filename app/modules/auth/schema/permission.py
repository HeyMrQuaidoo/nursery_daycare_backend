from uuid import UUID
from typing import List, Optional, Annotated
from pydantic import BaseModel, ConfigDict, constr


# models
from app.modules.auth.models.permissions import Permissions as PermissionsModel


class Role(BaseModel):
    role_id: Optional[UUID] = None
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PermissionBase(BaseModel):
    description: Optional[str] = None
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    # roles: Optional[Union[List[Role]]] = None #comment

    model_config = ConfigDict(from_attributes=True)


class Permission(PermissionBase):
    permission_id: Optional[UUID] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "permission_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Administrator",
                "alias": "admin",
                "description": "Has full access to all settings.",
            }
        },
    )


class PermissionCreateSchema(PermissionBase):
    model_config = ConfigDict(from_attributes=True)


class PermissionUpdateSchema(PermissionBase):
    model_config = ConfigDict(from_attributes=True)


class PermissionResponse(BaseModel):
    permission_id: UUID
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    description: Optional[str] = None
    roles: Optional[List[Role]] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, permission: PermissionsModel):
        """
        Create a PermissionResponse instance from an ORM model.

        Args:
            permission (PermissionsModel): Permission ORM model.

        Returns:
            PermissionResponse: Permission response object.
        """
        return cls(
            permission=permission.permission_id,
            name=permission.name,
            alias=permission.alias,
            description=permission.description,
            roles=permission.roles,
        ).model_dump()
