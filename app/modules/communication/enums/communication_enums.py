import enum


class CalendarStatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class EventTypeEnum(enum.Enum):
    other = "other"
    holiday = "holiday"
    meeting = "meeting"
    birthday = "birthday"
    inspection = "inspection"
    maintenance_request = "maintenance_request"


class MaintenanceStatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"
    in_progress = "in_progress"


class TourType(str, enum.Enum):
    in_person = "in_person"
    video = "video_chat"


class TourStatus(str, enum.Enum):
    incoming = "incoming"
    completed = "completed"
    cancelled = "cancelled"
