from uuid import UUID
from datetime import datetime
from typing import Any, Optional, Union

# schema
from app.modules.auth.schema.mixins.user_mixin import UserBase
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema


class AttendanceLogBase(BaseSchema):
    user_id: Optional[Union[UUID | UserBase]] = None
    check_in_time: Optional[datetime | Any] = None
    check_out_time: Optional[datetime | Any] = None
    date_stamp: Optional[datetime] = None


class AttendanceLog(AttendanceLogBase):
    attendance_id: Optional[UUID] = None


class AttendanceLogInfoMixin:
    _user_id = BaseFaker.uuid4()
    _check_in_time = BaseFaker.date_time_this_year()
    _check_out_time = BaseFaker.date_time_this_year()
    _date_stamp = BaseFaker.date_time_this_month()

    _attendance_log_create_json = {
        "user_id": _user_id,
        "check_in_time": _check_in_time,
        "check_out_time": _check_out_time,
        "date_stamp": _date_stamp,
    }

    _attendance_log_update_json = {
        "check_in_time": _check_in_time,
        "check_out_time": _check_out_time,
    }
