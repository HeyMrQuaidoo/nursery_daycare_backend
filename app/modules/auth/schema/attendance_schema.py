from uuid import UUID
from datetime import datetime
from pydantic import ConfigDict
from typing import Optional, Union

# models
from app.modules.auth.models.attendance import AttendanceLog as AttendanceLogModel

# schema
from app.modules.auth.schema.mixins.attendance_log_mixin import (
    AttendanceLog,
    AttendanceLogBase,
    AttendanceLogInfoMixin,
)
from app.modules.auth.schema.mixins.user_mixin import UserBase, UserBaseMixin


class AttendanceLogCreateSchema(AttendanceLog, AttendanceLogInfoMixin, UserBaseMixin):
    user_id: Optional[Union[UUID | UserBase]] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={datetime: lambda v: v.isoformat() if v else None},
        json_schema_extra={
            "example": AttendanceLogInfoMixin._attendance_log_create_json
        },
    )

    @classmethod
    def model_validate(
        cls, attendance_log: AttendanceLogModel
    ) -> "AttendanceLogResponse":
        return cls(
            attendance_id=attendance_log.attendance_id,
            user_id=cls.get_user_info(attendance_log.user),
            check_in_time=attendance_log.check_in_time,
            check_out_time=attendance_log.check_out_time,
            date_stamp=attendance_log.date_stamp,
        )


class AttendanceLogUpdateSchema(AttendanceLogBase, UserBaseMixin):
    user_id: Optional[Union[UUID | UserBase]] = None
    date_stamp: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={datetime: lambda v: v.isoformat() if v else None},
        json_schema_extra={
            "example": AttendanceLogInfoMixin._attendance_log_update_json
        },
    )

    @classmethod
    def model_validate(
        cls, attendance_log: AttendanceLogModel
    ) -> "AttendanceLogResponse":
        return cls(
            attendance_id=attendance_log.attendance_id,
            user_id=cls.get_user_info(attendance_log.user),
            check_in_time=attendance_log.check_in_time,
            check_out_time=attendance_log.check_out_time,
            date_stamp=attendance_log.date_stamp,
        )


class AttendanceLogResponse(AttendanceLogBase, UserBaseMixin):
    user_id: Optional[Union[UUID | UserBase]] = None
    attendance_id: UUID

    @classmethod
    def model_validate(
        cls, attendance_log: AttendanceLogModel
    ) -> "AttendanceLogResponse":
        return cls(
            attendance_id=attendance_log.attendance_id,
            user_id=cls.get_user_info(attendance_log.user),
            check_in_time=attendance_log.check_in_time,
            check_out_time=attendance_log.check_out_time,
            date_stamp=attendance_log.date_stamp,
        )
