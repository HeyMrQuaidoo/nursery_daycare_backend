import uuid
from sqlalchemy import UUID, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class Region(Base):
    __tablename__ = "region"

    region_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    country_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("country.country_id")
    )
    region_name: Mapped[str] = mapped_column(String(128))

    # city
    city: Mapped[list["City"]] = relationship("City", back_populates="region")

    # country
    country: Mapped["Country"] = relationship("Country", back_populates="region")

    # address
    addresses: Mapped[list["Addresses"]] = relationship(
        "Addresses", back_populates="region"
    )
