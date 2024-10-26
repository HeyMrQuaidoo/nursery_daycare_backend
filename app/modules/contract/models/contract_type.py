from typing import List
from sqlalchemy import Numeric, Integer, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base
from app.modules.contract.enums.contract_enums import ContractTypeEnum


class ContractType(Base):
    __tablename__ = "contract_type"

    contract_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, index=True, autoincrement=True
    )
    # contract_type_name: Mapped[str] = mapped_column(String(128))
    contract_type_name: Mapped[ContractTypeEnum] = mapped_column(
        Enum(ContractTypeEnum),
        unique=True,
        index=True,
    )
    fee_percentage: Mapped[float] = mapped_column(Numeric(5, 2))

    # contracts
    contracts: Mapped[List["Contract"]] = relationship(
        "Contract", back_populates="contract_type"
    )
