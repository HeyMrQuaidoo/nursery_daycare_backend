from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession


# dao
from app.modules.auth.dao.role_dao import RoleDAO
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.billing.dao.account_dao import AccountDAO
from app.modules.address.dao.address_dao import AddressDAO
from app.modules.forms.dao.answer_dao import AnswerDAO


# models
from app.modules.auth.models.user import User


class UserDAO(BaseDAO[User]):
    def __init__(self, excludes: Optional[List[str]] = []):
        self.model = User

        self.role_dao = RoleDAO()
        self.address_dao = AddressDAO()
        self.account_dao = AccountDAO()
        self.answer_dao = AnswerDAO()
        self.detail_mappings = {
            "address": self.address_dao,
            "roles": self.role_dao,
            "accounts": self.account_dao,
            "answers": self.answer_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="user_id",
        )

    async def user_exists(self, db_session: AsyncSession, email: str):
        return await self.query(
            db_session=db_session, filters={"email": email}, single=True
        )
