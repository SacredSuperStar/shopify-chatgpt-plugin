from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class EmailMarketingConsent(BaseModel):
    state: Optional[str]
    opt_in_level: Optional[str]
    consent_updated_at: Optional[str]


class SmsMarketingConsent(BaseModel):
    state: Optional[str]
    opt_in_level: Optional[str]
    consent_updated_at: Optional[str]
    consent_collected_from: Optional[str]


class Customer(BaseModel):
    id: Optional[int]
    email: Optional[str]
    accepts_marketing: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    orders_count: Optional[int]
    state: Optional[str]
    total_spent: Optional[str]
    last_order_id: Optional[int]
    note: Optional[str]
    verified_email: Optional[bool]
    tags: Optional[str]
    last_order_name: Optional[str]
    accepts_marketing_updated_at: Optional[datetime]
    marketing_opt_in_level: Optional[str]
    email_marketing_consent: Optional[EmailMarketingConsent]
    sms_marketing_consent: Optional[SmsMarketingConsent]


class DiscountCode(BaseModel):
    code: Optional[str]
    amount: Optional[str]
    type: Optional[str]


class Order(BaseModel):
    id: Optional[int]
    customer: Optional[Customer]
    buyer_accepts_marketing: Optional[bool]
    cancel_reason: Optional[str]
    cancelled_at: Optional[str]
    closed_at: Optional[str]
    confirmed: Optional[bool]
    created_at: Optional[datetime]
    currency: Optional[str]
    current_subtotal_price: Optional[str]
    current_total_discounts: Optional[str]
    current_total_duties_set: Optional[str]
    current_total_price: Optional[str]
    current_total_tax: Optional[str]
    discount_codes: Optional[list[DiscountCode]]
    estimated_taxes: Optional[bool]
    financial_status: Optional[str]
    fulfillment_status: Optional[str]
    name: Optional[str]
    note: Optional[str]
    processed_at: Optional[datetime]
    source_url: Optional[str]
    subtotal_price: Optional[str]
    tags: Optional[str]
    taxes_included: Optional[bool]
    total_discounts: Optional[str]
    total_line_items_price: Optional[str]
    total_outstanding: Optional[str]
    total_price: Optional[str]
    total_tax: Optional[str]
    total_tip_received: Optional[str]
    total_weight: Optional[int]
    updated_at: Optional[datetime]
    refunds: Optional[list]


class ApiKeyBase(BaseModel):
    key: Optional[str]
    shop_id: Optional[int]
    last_used_at: Optional[datetime]
    last_used_ip: Optional[str]
    last_used_user_agent: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class ApiKey(ApiKeyBase):
    id = int

    class Config:
        orm_mode = True


class ShopBase(BaseModel):
    shopify_domain: Optional[str]
    shopify_token: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    access_scopes: Optional[str]


class Shop(ShopBase):
    id: int
    api_keys: Optional[list[ApiKey]]

    class Config:
        orm_mode = True