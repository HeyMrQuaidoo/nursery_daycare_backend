import uuid
from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class RolePermissions(Base):
    __tablename__ = "role_permissions"

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("role.role_id"), primary_key=True
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("permissions.permission_id"), primary_key=True
    )
