import enum


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class UserRoleEnum(enum.Enum):
    admin = "admin"
    user = "user"
    guest = "guest"
    manager = "manager"
