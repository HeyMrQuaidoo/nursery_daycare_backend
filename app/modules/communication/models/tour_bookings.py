import uuid
import pytz
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import UUID, String, Enum, DateTime, ForeignKey

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.communication.enums.communication_enums import TourStatus, TourType


class Tour(Base):
    __tablename__ = "tour"

    tour_booking_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)
    tour_type: Mapped[TourType] = mapped_column(
        Enum(TourType), default=TourType.in_person, nullable=True, name="tour_type"
    )
    status: Mapped[TourStatus] = mapped_column(
        Enum(TourStatus),
        default=TourStatus.incoming,
        nullable=True,
        name="status",
    )
    tour_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    # property_unit_assoc_id: Mapped[uuid.UUID] = mapped_column(
    #     UUID(as_uuid=True),
    #     ForeignKey("property_unit_assoc.property_unit_assoc_id", ondelete="CASCADE"),
    # )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=True,
    )

    # user
    user: Mapped["User"] = relationship("User", back_populates="tours", lazy="selectin")
