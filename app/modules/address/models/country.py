import uuid
from sqlalchemy import String, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class Country(Base):
    __tablename__ = "country"

    country_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    country_name: Mapped[str] = mapped_column(String(128), unique=True)

    # region
    region: Mapped[list["Region"]] = relationship("Region", back_populates="country")

    # address
    addresses: Mapped[list["Addresses"]] = relationship(
        "Addresses", back_populates="country"
    )
