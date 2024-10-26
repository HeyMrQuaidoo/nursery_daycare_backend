import enum


class ContractStatusEnum(enum.Enum):
    active = "active"
    inactive = "inactive"
    expired = "expired"
    pending = "pending"
    terminated = "terminated"


class ContractTypeEnum(enum.Enum):
    rent = "rent"
    lease = "lease"
    purchase = "purchase"
    sale = "sale"
