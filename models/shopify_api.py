from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional


class FinancialStatusForOrderCount(str, Enum):
    authorized = "authorized"
    pending = "pending"
    paid = "paid"
    refunded = "refunded"
    voided = "voided"
    any = "any"

class FinancialStatus(str, Enum):
    authorized = "authorized"
    pending = "pending"
    paid = "paid"
    partially_paid = "partially_paid"
    refunded = "refunded"
    voided = "voided"
    partially_refunded = "partially_refunded"
    any = "any"
    unpaid = "unpaid"


class FulfillmentStatus(str, Enum):
    shipped = "shipped"
    partial = "partial"
    unshipped = "unshipped"
    any = "any"
    unfulfilled = "unfulfilled"


class OrderCountStatus(str, Enum):
    open = "open"
    closed = "closed"
    any = "any"

class OrderStatus(str, Enum):
    open = "open"
    closed = "closed"
    cancelled = "cancelled"
    any = "any"


class OrderCountUrlParams(BaseModel):
    created_at_max: datetime = None
    created_at_min: datetime = None
    financial_status: FinancialStatusForOrderCount = FinancialStatusForOrderCount.any
    fulfillment_status: FulfillmentStatus = FulfillmentStatus.any
    status: OrderCountStatus = OrderCountStatus.open
    updated_at_max: datetime = None
    updated_at_min: datetime = None


class OrderUrlParams(BaseModel):
    attribution_app_id: str = None
    created_at_max: datetime = None
    created_at_min: datetime = None
    fields: str = None
    financial_status: FinancialStatus = FinancialStatus.any
    fulfillment_status: FulfillmentStatus = FulfillmentStatus.any
    ids: str = None
    limit: int = 50
    processed_at_max: datetime = None
    processed_at_min: datetime = None
    since_id: int = None
    status: OrderCountStatus = OrderCountStatus.open
    updated_at_max: datetime = None
    updated_at_min: datetime = None


class CustomerCountUrlParams(BaseModel):
    created_at_max: datetime = None
    created_at_min: datetime = None
    updated_at_max: datetime = None
    updated_at_min: datetime = None


class SearchOrderDirection(str, Enum):
    asc = "ASC"
    desc = "DESC"


class CustomerSearchUrlParams(BaseModel):
    fields: str = None
    limit: int = 50
    order_field: Optional[str] = "last_order_date"
    order_direction: SearchOrderDirection = SearchOrderDirection.desc
    query: Optional[str] = None