from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import List, Optional

# enums
from app.modules.contract.enums.contract_enums import ContractStatusEnum
from app.modules.billing.enums.billing_enums import InvoiceTypeEnum, PaymentStatusEnum

# schema
from app.modules.common.schema.base_schema import BaseFaker
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.auth.schema.mixins.user_mixin import UserBaseMixin
from app.modules.resources.schema.mixins.media_mixin import MediaBase
from app.modules.billing.schema.mixins.invoice_mixin import InvoiceBase
from app.modules.contract.schema.mixins.under_contract_mixin import UnderContract
from app.modules.contract.schema.mixins.under_contract_mixin import UnderContractBase

from app.modules.billing.schema.invoice_schema import InvoiceResponse
from app.modules.resources.schema.media_schema import MediaResponse

# models
from app.modules.contract.models.contract import Contract as ContractModel
from app.modules.billing.models.payment_type import PaymentType as PaymentTypeModel
from app.modules.contract.models.contract_type import ContractType as ContractTypeModel
from app.modules.contract.models.under_contract import (
    UnderContract as UnderContractModel,
)


class ContractBase(BaseSchema):
    contract_type_id: int
    payment_type_id: int
    contract_status: Optional[ContractStatusEnum]
    contract_details: Optional[str] = None
    num_invoices: Optional[int]
    payment_amount: Optional[Decimal]
    fee_percentage: Optional[Decimal] = None
    fee_amount: Optional[Decimal]
    date_signed: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    invoices: Optional[List[InvoiceBase]] = None
    under_contract: Optional[List[UnderContractBase]] = None
    media: Optional[List[MediaBase]] = None


class Contract(BaseSchema):
    contract_number: Optional[str] = None
    contract_id: UUID


class ContractInfoMixin(UserBaseMixin):
    # base attributes
    _contract_type_id = BaseFaker.random_int(min=1, max=1)
    _payment_type_id = BaseFaker.random_int(min=1, max=1)
    _contract_status = BaseFaker.random_element([e.value for e in ContractStatusEnum])
    _contract_details = BaseFaker.text(max_nb_chars=200)
    _num_invoices = BaseFaker.random_int(min=1, max=10)
    _payment_amount = round(BaseFaker.random_number(digits=5), 2)
    _fee_percentage = round(BaseFaker.random_number(digits=2), 2)
    _fee_amount = round(BaseFaker.random_number(digits=4), 2)
    _date_signed = BaseFaker.date_this_year()
    _start_date = BaseFaker.date_this_year()
    _end_date = BaseFaker.future_date()

    # utilities
    _utility_name = BaseFaker.word()
    _utility_description = BaseFaker.text(max_nb_chars=100)
    _billable_amount = round(BaseFaker.random_number(digits=4), 2)
    _apply_to_units = BaseFaker.boolean()
    _invoice_number = BaseFaker.bothify(text="INV-#####")
    _invoice_amount = round(BaseFaker.random_number(digits=2), 2)

    # media
    _media_name = BaseFaker.word()
    _media_type = BaseFaker.random_element(["image", "video", "document"])
    _invoice_type = BaseFaker.random_element([e.value for e in InvoiceTypeEnum])
    _status = BaseFaker.random_element([e.value for e in PaymentStatusEnum])

    _contract_create_json = {
        "contract_type_id": _contract_type_id,
        "payment_type_id": _payment_type_id,
        "contract_status": _contract_status,
        "contract_details": _contract_details,
        "num_invoices": _num_invoices,
        "payment_amount": _payment_amount,
        "fee_percentage": _fee_percentage,
        "fee_amount": _fee_amount,
        "date_signed": _date_signed.isoformat(),
        "start_date": _start_date.isoformat(),
        "end_date": _end_date.isoformat(),
        "utilities": [
            {
                "name": _utility_name,
                "description": _utility_description,
                "billable_type": "utilities",
                "billable_amount": _billable_amount,
                "apply_to_units": _apply_to_units,
                "payment_type_id": _payment_type_id,
                "start_period": _start_date.isoformat(),
                "end_period": _end_date.isoformat(),
            }
        ],
        "invoices": [
            {
                "issued_by": "d0e356e8-4a7f-43ed-b395-3366a773ab19",
                "issued_to": "d0e356e8-4a7f-43ed-b395-3366a773ab19",
                "invoice_details": BaseFaker.text(max_nb_chars=200),
                "invoice_amount": _invoice_amount,
                "due_date": BaseFaker.future_datetime().isoformat(),
                "invoice_type": _invoice_type,
                "status": _status,
                "invoice_items": [
                    {
                        "description": BaseFaker.sentence(),
                        "quantity": BaseFaker.random_int(min=1, max=10),
                        "unit_price": round(BaseFaker.random_number(digits=5), 2),
                        "reference_id": str(BaseFaker.uuid4()),
                    }
                ],
            }
        ],
        "under_contract": [
            {
                "property_unit_assoc_id": "b9f0ba78-34b3-4e5d-811c-5d84ed1cacd9",
                "contract_status": _contract_status,
                "client_id": "d0e356e8-4a7f-43ed-b395-3366a773ab19",
                "employee_id": "d0e356e8-4a7f-43ed-b395-3366a773ab19",
                "start_date": _start_date.isoformat(),
                "end_date": _end_date.isoformat(),
                "next_payment_due": BaseFaker.future_datetime().isoformat(),
            }
        ],
        "media": [
            {
                "media_name": _media_name,
                "media_type": _media_type,
                "content_url": BaseFaker.url(),
                "is_thumbnail": BaseFaker.boolean(),
                "caption": BaseFaker.sentence(),
                "description": BaseFaker.text(max_nb_chars=200),
            }
        ],
    }

    _contract_update_json = {
        "contract_type_id": _contract_type_id,
        "payment_type_id": _payment_type_id,
        "contract_status": _contract_status,
        "contract_details": _contract_details,
        "num_invoices": _num_invoices,
        "payment_amount": _payment_amount,
        "fee_percentage": _fee_percentage,
        "fee_amount": _fee_amount,
        "date_signed": _date_signed.isoformat(),
        "start_date": _start_date.isoformat(),
        "end_date": _end_date.isoformat(),
        "utilities": [
            {
                "name": _utility_name,
                "description": _utility_description,
                "billable_type": "utilities",
                "billable_amount": _billable_amount,
                "apply_to_units": _apply_to_units,
                "payment_type_id": _payment_type_id,
                "start_period": _start_date.isoformat(),
                "end_period": _end_date.isoformat(),
            }
        ],
        "invoices": [
            {
                "issued_by": "d0e356e8-4a7f-43ed-b395-3366a773ab19",
                "issued_to": "d0e356e8-4a7f-43ed-b395-3366a773ab19",
                "invoice_details": BaseFaker.text(max_nb_chars=200),
                "invoice_amount": _invoice_amount,
                "due_date": BaseFaker.future_datetime().isoformat(),
                "invoice_type": _invoice_type,
                "status": _status,
                "invoice_items": [
                    {
                        "invoice_item_id": str(
                            BaseFaker.uuid4()
                        ),  # Added this not on create_json
                        "description": BaseFaker.sentence(),
                        "quantity": BaseFaker.random_int(min=1, max=10),
                        "unit_price": round(BaseFaker.random_number(digits=5), 2),
                        "reference_id": str(BaseFaker.uuid4()),
                    }
                ],
            }
        ],
        "under_contract": [
            {
                "under_contract_id": str(
                    BaseFaker.uuid4()
                ),  # Added this not on create_json
                "property_unit_assoc_id": "402c0deb-b978-40d6-a269-c690cbd99589",
                "contract_status": _contract_status,
                "client_id": "d0e356e8-4a7f-43ed-b395-3366a773ab19",
                "employee_id": "d0e356e8-4a7f-43ed-b395-3366a773ab19",
                "start_date": _start_date.isoformat(),
                "end_date": _end_date.isoformat(),
                "next_payment_due": BaseFaker.future_datetime().isoformat(),
            }
        ],
        "media": [
            {
                "media_id": str(BaseFaker.uuid4()),  # Added this not on create_json
                "media_name": _media_name,
                "media_type": _media_type,
                "content_url": BaseFaker.url(),
                "is_thumbnail": BaseFaker.boolean(),
                "caption": BaseFaker.sentence(),
                "description": BaseFaker.text(max_nb_chars=200),
            }
        ],
    }

    @classmethod
    def get_contract_details(cls, contract_details: List[UnderContractModel]):
        result = []

        for contract_detail in contract_details:
            result.append(
                UnderContract(
                    under_contract_id=contract_detail.under_contract_id,
                    contract_number=contract_detail.contract_number,
                    contract_status=contract_detail.contract_status,
                    client_representative=cls.get_user_info(
                        contract_detail.client_representative
                    ),
                    employee_representative=cls.get_user_info(
                        contract_detail.employee_representative
                    ),
                    start_date=contract_detail.start_date,
                    end_date=contract_detail.end_date,
                    next_payment_due=contract_detail.next_payment_due,
                ).model_dump(exclude=["client_id", "employee_id"])
            )

        return result

    @classmethod
    def get_contract_info(
        cls, contract_info: List[UnderContractModel]
    ) -> List[Contract]:
        result = []

        for under_contract in contract_info:
            contract: ContractModel = under_contract.contract

            if contract:
                # Fetch related contract_type and payment_type
                contract_type: ContractTypeModel = contract.contract_type
                payment_type: PaymentTypeModel = contract.payment_type

                result.append(
                    Contract(
                        contract_id=contract.contract_id,
                        contract_number=contract.contract_number,
                        num_invoices=contract.num_invoices,
                        contract_type=contract_type.contract_type_name
                        if contract_type
                        else None,  # Fetch contract type name
                        payment_type=payment_type.payment_type_name
                        if payment_type
                        else None,  # Fetch payment type name
                        contract_status=contract.contract_status,
                        contract_details=contract.contract_details,
                        payment_amount=contract.payment_amount,
                        fee_percentage=contract.fee_percentage,
                        fee_amount=contract.fee_amount,
                        date_signed=contract.date_signed,
                        start_date=contract.start_date,
                        end_date=contract.end_date,
                        next_payment_due=under_contract.next_payment_due,
                    )
                )
        return result

    @classmethod
    def get_invoices_info(cls, invoices):
        return (
            [InvoiceResponse.model_validate(invoice) for invoice in invoices]
            if invoices
            else []
        )

    @classmethod
    def get_media_info(cls, media_items):
        return (
            [MediaResponse.model_validate(media) for media in media_items]
            if media_items
            else []
        )
