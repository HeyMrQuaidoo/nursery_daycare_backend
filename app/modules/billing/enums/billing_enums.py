import enum


class AccountTypeEnum(enum.Enum):
    savings = "savings"
    billing = "billing"
    debit = "debit"
    credit = "credit"
    general = "general"


class CompanyTypeEnum(enum.Enum):
    agency = "agency"
    sole_proprietor = "sole_proprietor"


class BillableTypeEnum(enum.Enum):
    utilities = "utilities"
    maintenance_requests = "maintenance_requests"


class PaymentStatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"
    reversal = "reversal"


class InvoiceTypeEnum(enum.Enum):
    lease = "lease"
    maintenance = "maintenance"
    other = "other"
    general = "general"


class PaymentTypeEnum(enum.Enum):
    annually = "annually"
    monthly = "monthly"
    weekly = "weekly"
    one_time = "one_time"
    quarterly = "quarterly"
    bi_annual = "bi_annual"
    custom = "custom"


class TransactionTypeEnum(enum.Enum):
    card = "card"
    mobile_money = "mobile_money"
    visa = "visa"
    paypal = "paypal"
    refund = "refund"
    credit = "credit"
    debit = "debit"
    bank_transfer = "bank_transfer"
    cash = "cash"
    cryptocurrency = "cryptocurrency"
    check = "check"
    direct_debit = "direct_debit"
    ewallet = "ewallet"
    prepaid_card = "prepaid_card"
    net_banking = "net_banking"
    wire_transfer = "wire_transfer"
    pos = "pos"
    google_pay = "google_pay"
    apple_pay = "apple_pay"
    stripe = "stripe"
    square = "square"
