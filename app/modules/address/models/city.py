import uuid
from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class City(Base):
    __tablename__ = "city"

    city_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    region_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("region.region_id")
    )
    city_name: Mapped[str] = mapped_column(String(128))

    # region
    region: Mapped["Region"] = relationship("Region", back_populates="city")

    # address
    addresses: Mapped[list["Addresses"]] = relationship(
        "Addresses", back_populates="city"
    )
