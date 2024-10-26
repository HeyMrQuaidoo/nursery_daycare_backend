import uuid
from typing import List
from sqlalchemy import String, Text, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class Permissions(Base):
    __tablename__ = "permissions"

    permission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(80), unique=True)
    alias: Mapped[str] = mapped_column(String(80), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # roles
    roles: Mapped[List["Role"]] = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions",
        lazy="selectin",
    )


# register model
Base.setup_model_dynamic_listener("role_permissions", Permissions)
