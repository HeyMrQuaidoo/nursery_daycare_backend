from pydantic import UUID4
from typing import List, Optional, Union

# enums
from app.modules.billing.enums.billing_enums import AccountTypeEnum

# schemas
from app.modules.address.schema.address_schema import AddressBase
from app.modules.billing.schema.mixins.account_mixin import AccountMixin, AccountBase


# models
from app.modules.billing.models.account import Account as AccountModel


class AccountResponse(AccountMixin):
    account_id: Optional[UUID4] = None
    account_type: Optional[Union[AccountTypeEnum | List[AccountTypeEnum]]] = None
    bank_account_name: str
    bank_account_number: str
    account_branch_name: str
    address: Optional[List[AddressBase]] = []

    @classmethod
    def model_validate(cls, accounts: Union[AccountModel | List[AccountModel]]):
        return cls.get_account_info(accounts)


class AccountCreateSchema(AccountBase, AccountMixin):
    address: Optional[List[AddressBase]]

    @classmethod
    def model_validate(cls, accounts: Union[AccountModel | List[AccountModel]]):
        return cls.get_account_info(accounts)


class AccountUpdateSchema(AccountBase):
    address: Optional[List[AddressBase]]

    @classmethod
    def model_validate(cls, accounts: Union[AccountModel | List[AccountModel]]):
        return cls.get_account_info(accounts)
