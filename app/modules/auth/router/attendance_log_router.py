from typing import List
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# core
from app.core.response import DAOResponse
from app.core.errors import CustomException

# models
from app.modules.auth.models.user import User
from app.modules.auth.models.attendance import AttendanceLog

# enums
from app.modules.auth.enums.user_enums import AttendanceLogType

# dao
from app.modules.auth.dao.user_dao import UserDAO
from app.modules.auth.dao.attendance_dao import AttendanceLogDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schema
from app.modules.common.schema.schemas import AttendanceLogSchema
from app.modules.auth.schema.attendance_schema import (
    AttendanceLogCreateSchema,
    AttendanceLogUpdateSchema,
)
from app.modules.auth.schema.mixins.attendance_log_mixin import GuestAttendance


class AttendanceLogRouter(BaseCRUDRouter):
    def __init__(
        self, prefix: str = "/attendance_logs", tags: List[str] = ["Attendance Logs"]
    ):
        self.dao: AttendanceLogDAO = AttendanceLogDAO(excludes=[])
        self.user_dao: UserDAO = UserDAO()

        AttendanceLogSchema["create_schema"] = AttendanceLogCreateSchema
        AttendanceLogSchema["update_schema"] = AttendanceLogUpdateSchema

        super().__init__(
            dao=self.dao, schemas=AttendanceLogSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        @self.router.post("/guest-attendance")
        async def guest_attendance(
            request: GuestAttendance, db: AsyncSession = Depends(self.get_db)
        ):
            try:
                current_user: User = await self.user_dao.user_exists(
                    db_session=db, email=request.email
                )

                if current_user is None:
                    raise HTTPException(status_code=401, detail="User not found")
                else:
                    # Get today's date boundaries
                    today_start = datetime.now().replace(
                        hour=0, minute=0, second=0, microsecond=0
                    )
                    today_end = today_start + timedelta(days=1)

                    # Check if the user has an attendance log for today
                    existing_log: AttendanceLog = await self.dao.query(
                        db_session=db,
                        filters={
                            "user_id": current_user.user_id,
                            "date_stamp": {"$gte": today_start, "$lt": today_end},
                        },
                        single=True,
                    )

                    if request.attendance_type == AttendanceLogType.check_in.name:
                        if existing_log is None:
                            # No check-in exists for today, create a new attendance log
                            new_log_data = {
                                "user_id": current_user.user_id,
                                "check_in_time": datetime.now(),
                            }
                            await self.dao.create(db_session=db, obj_in=new_log_data)
                            return DAOResponse(
                                success=True, data="Check-in recorded successfully."
                            )
                        else:
                            return DAOResponse(
                                success=True,
                                data="User is already checked in for today.",
                            )

                    elif request.attendance_type == AttendanceLogType.check_out.name:
                        if existing_log and existing_log.check_out_time is None:
                            # User has checked in but not checked out, log check-out time
                            await self.dao.update(
                                db_session=db,
                                db_obj=existing_log,
                                obj_in={"check_out_time": datetime.now()},
                            )
                            return DAOResponse(
                                success=True, data="Check-out recorded successfully."
                            )
                        elif existing_log:
                            return DAOResponse(
                                success=True,
                                data="User has already checked out for today.",
                            )
                        else:
                            return DAOResponse(
                                success=True,
                                data="User has not checked in yet, so check-out is not possible.",
                            )
                    else:
                        raise HTTPException(
                            status_code=400, detail="Invalid attendance type"
                        )
            except Exception as e:
                raise CustomException(e)

        @self.router.post("/guest-attendance/{user_id}")
        async def guest_attendance_by_id(
            user_id: str,
            request: GuestAttendance,
            db: AsyncSession = Depends(self.get_db),
        ):
            try:
                current_user: User = await self.user_dao.user_exists(
                    db_session=db, filters={"user_id": user_id}, single=True
                )

                if current_user is None:
                    raise HTTPException(status_code=401, detail="User not found")
                else:
                    # Get today's date boundaries
                    today_start = datetime.now().replace(
                        hour=0, minute=0, second=0, microsecond=0
                    )
                    today_end = today_start + timedelta(days=1)

                    # Check if the user has an attendance log for today
                    existing_log: AttendanceLog = await self.dao.query(
                        db_session=db,
                        filters={
                            "user_id": current_user.user_id,
                            "date_stamp": {"$gte": today_start, "$lt": today_end},
                        },
                        single=True,
                    )

                    if request.attendance_type == AttendanceLogType.check_in.name:
                        if existing_log is None:
                            # No check-in exists for today, create a new attendance log
                            new_log_data = {
                                "user_id": current_user.user_id,
                                "check_in_time": datetime.now(),
                            }
                            await self.dao.create(db_session=db, obj_in=new_log_data)
                            return DAOResponse(
                                success=True, data="Check-in recorded successfully."
                            )
                        else:
                            return DAOResponse(
                                success=True,
                                data="User is already checked in for today.",
                            )

                    elif request.attendance_type == AttendanceLogType.check_out.name:
                        if existing_log and existing_log.check_out_time is None:
                            # User has checked in but not checked out, log check-out time
                            await self.dao.update(
                                db_session=db,
                                db_obj=existing_log,
                                obj_in={"check_out_time": datetime.now()},
                            )
                            return DAOResponse(
                                success=True, data="Check-out recorded successfully."
                            )
                        elif existing_log:
                            return DAOResponse(
                                success=True,
                                data="User has already checked out for today.",
                            )
                        else:
                            return DAOResponse(
                                success=True,
                                data="User has not checked in yet, so check-out is not possible.",
                            )
                    else:
                        raise HTTPException(
                            status_code=400, detail="Invalid attendance type"
                        )
            except Exception as e:
                raise CustomException(e)
