import enum


class PriorityEnum(enum.Enum):
    low = "low"
    high = "high"
    medium = "medium"
    on_hold = "on_hold"
    trivial = "trivial"
    blocker = "blocker"
    deferred = "deferred"
    critical = "critical"
