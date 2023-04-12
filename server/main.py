import os
import uvicorn
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
load_dotenv()

from models.shopify_api import(
    OrderCountUrlParams, 
    OrderUrlParams,
    CustomerCountUrlParams,
    CustomerSearchUrlParams,
)
from models.api import (
    CountResponse,
    CustomersResponse,
    CustomerResponse,
    OrdersResponse,
    OrderResponse,
)

from services.shopify import (
    get_shop_order,
    get_shop_orders,
    get_shop_orders_count,
    get_shop_customer,
    get_shop_customers,
    get_shop_customers_count,
    DEFAULT_CUSTOMER_FIELDS,
    DEFAULT_ORDER_FIELDS,
)

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST")
SHOP_NAME = os.getenv("SHOP_NAME")
SHOP_DOMAIN_NAME = os.getenv("SHOP_DOMAIN_NAME")
SHOP_API_KEY = os.getenv("SHOP_API_KEY")
assert HOST is not None
assert SHOP_NAME is not None
assert SHOP_DOMAIN_NAME is not None
assert SHOP_API_KEY is not None

bearer_scheme = HTTPBearer()
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
assert BEARER_TOKEN is not None


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.scheme != "Bearer" or credentials.credentials != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials

origins = [
    HOST,
    "https://chat.openai.com",
]

if HOST == "http://localhost:8000":
    api_dependencies = []
else:
    api_dependencies = [Depends(validate_token)]

app = FastAPI(
    title=f"{SHOP_NAME} Store Admin Plugin API",
    description=f"An API for querying and looking up information about {SHOP_NAME}'s orders and customers.",
    version="1.0.0",
    servers=[{"url": HOST}],
    dependencies=api_dependencies,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if HOST == "http://localhost:8000":
    app.mount("/.well-known", StaticFiles(directory="local-server", html=True), name="static")
else:
    app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")


@app.get(
    "/orders", 
    response_model=OrdersResponse,
    response_model_exclude_unset=True
)
async def get_orders(
    attribution_app_id: str | None = None,
    created_at_max: datetime | None = None,
    created_at_min: datetime | None = None,
    fields: str | None = DEFAULT_ORDER_FIELDS,
    financial_status: str = "any",
    fulfillment_status: str = "any",
    ids: str | None = None,
    limit: int = 10,
    processed_at_max: datetime | None = None,
    processed_at_min: datetime | None = None,
    since_id: int | None = None,
    status: str = "open",
    updated_at_max: datetime | None = None,
    updated_at_min: datetime | None = None,
):
    try:
        orders = get_shop_orders(SHOP_API_KEY, SHOP_DOMAIN_NAME, OrderUrlParams(
            attribution_app_id=attribution_app_id,
            created_at_max=created_at_max,
            created_at_min=created_at_min,
            fields=fields,
            financial_status=financial_status,
            fulfillment_status=fulfillment_status,
            ids=ids,
            limit=limit,
            processed_at_max=processed_at_max,
            processed_at_min=processed_at_min,
            since_id=since_id,
            status=status,
            updated_at_max=updated_at_max,
            updated_at_min=updated_at_min,
        ))
        return orders
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"str({e})")


@app.get(
    "/orders/count", 
    response_model=CountResponse,
    response_model_exclude_unset=True
)
async def get_orders_count(    
    created_at_max: datetime | None = None,
    created_at_min: datetime | None = None,
    financial_status: str | None = "any",
    fulfillment_status: str | None = "any",
    status: str | None = "open",
    updated_at_max: datetime | None = None,
    updated_at_min: datetime | None = None,
):
    try:
        orders_count = get_shop_orders_count(SHOP_API_KEY, SHOP_DOMAIN_NAME, OrderCountUrlParams(
            created_at_max=created_at_max,
            created_at_min=created_at_min,
            financial_status=financial_status,
            fulfillment_status=fulfillment_status,
            status=status,
            updated_at_max=updated_at_max,
            updated_at_min=updated_at_min,
        ))
        return orders_count
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"str({e})")


@app.get(
    "/orders/{order_id}", 
    response_model=OrderResponse,
    response_model_exclude_unset=True
)
async def get_order(
    order_id: int, 
    fields: str | None = DEFAULT_ORDER_FIELDS, 
):
    try:
        order = get_shop_order(SHOP_API_KEY, SHOP_DOMAIN_NAME, order_id, fields=fields)
        return order
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"str({e})")


@app.get(
    "/customers/count", 
    response_model=CountResponse
)
async def get_customers_count(
    created_at_max: datetime | None = None,
    created_at_min: datetime | None = None,
    updated_at_max: datetime | None = None,
    updated_at_min: datetime | None = None,
):
    try:
        customers_count = get_shop_customers_count(SHOP_API_KEY, SHOP_DOMAIN_NAME, CustomerCountUrlParams(
            created_at_max=created_at_max,
            created_at_min=created_at_min,
            updated_at_max=updated_at_max,
            updated_at_min=updated_at_min,
        ))

        return customers_count
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"str({e})")


@app.get(
    "/customers/search", 
    response_model=CustomersResponse,
    response_model_exclude_unset=True
)
async def search_customers(
    fields: str | None = DEFAULT_CUSTOMER_FIELDS,
    limit: int = 10,
    order_field: str = "last_order_date",
    order_direction: str = "DESC",
    query: str = None,
):
    try:
        customers = get_shop_customers(SHOP_API_KEY, SHOP_DOMAIN_NAME, CustomerSearchUrlParams(
            fields=fields,
            limit=limit,
            order_field=order_field,
            order_direction=order_direction,
            query=query,
        ))

        return customers
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"str({e})")


@app.get(
    "/customers/{customer_id}", 
    response_model=CustomerResponse,
    response_model_exclude_unset=True
)
async def get_customer(
    customer_id: int, 
    fields: str | None = DEFAULT_CUSTOMER_FIELDS, 
):
    try:
        customer = get_shop_customer(SHOP_API_KEY, SHOP_DOMAIN_NAME, customer_id, fields)
        return customer
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"str({e})")


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=PORT, reload=True)