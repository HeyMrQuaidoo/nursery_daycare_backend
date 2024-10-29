from fastapi import APIRouter, FastAPI

from app.modules.auth.router.role_router import RoleRouter
from app.modules.auth.router.user_router import UserRouter
from app.modules.auth.router.auth_router import AuthRouter
from app.modules.auth.router.permission_router import PermissionRouter
from app.modules.forms.router.answer_router import AnswerRouter
from app.modules.forms.router.question_router import QuestionRouter
from app.modules.forms.router.questionnaire_router import QuestionnaireRouter
from app.modules.auth.router.attendance_log_router import AttendanceLogRouter

router = APIRouter()


def configure_routes(app: FastAPI):
    app.include_router(router)

    # Create an instance of AuthRouter
    app.include_router(AuthRouter(prefix="/auth", tags=["Auth"]).router)

    # Create an instance of RoleRouter
    app.include_router(RoleRouter(prefix="/roles", tags=["Roles"]).router)

    # Create an instance of PermissionRouter
    app.include_router(
        PermissionRouter(prefix="/permissions", tags=["Permissions"]).router
    )

    # Create an instance of UserRouter
    app.include_router(UserRouter(prefix="/users", tags=["Users"]).router)

    # Create an instance of AnswerRouter
    app.include_router(
        QuestionnaireRouter(prefix="/questionnaire", tags=["Questionnaire"]).router
    )

    # Create an instance of QuestionRouter
    app.include_router(QuestionRouter(prefix="/questions", tags=["Questions"]).router)

    # # Create an instance of AnswerRouter
    app.include_router(AnswerRouter(prefix="/answers", tags=["Answers"]).router)

    # Create an instance of AttendanceRouter
    app.include_router(
        AttendanceLogRouter().router
    )
