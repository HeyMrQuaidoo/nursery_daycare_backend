from typing import List

# dao
from app.modules.auth.dao.attendance_dao import AttendanceLogDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schema
from app.modules.common.schema.schemas import AttendanceLogSchema
from app.modules.auth.schema.attendance_schema import (
    AttendanceLogCreateSchema,
    AttendanceLogUpdateSchema,
)

class AttendanceLogRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "/attendance_logs", tags: List[str] = ["Attendance Logs"]):
        self.dao: AttendanceLogDAO = AttendanceLogDAO(excludes=[])


        AttendanceLogSchema["create_schema"] = AttendanceLogCreateSchema
        AttendanceLogSchema["update_schema"] = AttendanceLogUpdateSchema

        super().__init__(
            dao=self.dao,
            schemas=AttendanceLogSchema,
            prefix=prefix,
            tags=tags
        )
        self.register_routes()

    def register_routes(self):
        pass
