from pydantic import BaseModel
from models.models import (
    Customer,
    Order,
)

class CountResponse(BaseModel):
    count: int


class CustomersResponse(BaseModel):
    customers: list[Customer]


class CustomerResponse(BaseModel):
    customer: Customer


class OrderResponse(BaseModel):
    order: Order


class OrdersResponse(BaseModel):
    orders: list[Order]