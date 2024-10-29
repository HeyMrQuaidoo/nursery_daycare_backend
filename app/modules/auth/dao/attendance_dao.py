from typing import List, Optional

# models
from app.modules.auth.models.attendance import AttendanceLog

# dao
from app.modules.auth.dao.user_dao import UserDAO
from app.modules.common.dao.base_dao import BaseDAO


class AttendanceLogDAO(BaseDAO[AttendanceLog]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = AttendanceLog

        self.user_dao = UserDAO()

        self.detail_mappings = {"user": self.user_dao}
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="attendance_id",
        )
