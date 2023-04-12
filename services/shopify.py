import requests
from urllib.parse import urlencode

from models.shopify_api import (
    OrderCountUrlParams, 
    OrderUrlParams,
    CustomerCountUrlParams,
    CustomerSearchUrlParams,
)

SHOPIFY_API_VERSION = "2022-10" # 2023-04 is latest version

# For better results, narrow fields returned
DEFAULT_ORDER_FIELDS = "id,buyer_accepts_marketing,cancel_reason,cancelled_at,closed_at,confirmed,created_at,total_price,updated_at"
ORDER_FIELDS = "id,customer,buyer_accepts_marketing,cancel_reason,cancelled_at,closed_at,confirmed,created_at,currency,current_subtotal_price,current_total_discounts,current_total_duties_set,current_total_price,current_total_tax,discount_codes,estimated_taxes,financial_status,fulfillment_status,name,note,processed_at,source_url,subtotal_price,tags,taxes_included,total_discounts,total_line_items_price,total_outstanding,total_price,total_tax,total_tip_received,total_weight,updated_at,refunds"
DEFAULT_CUSTOMER_FIELDS = "id,accepts_marketing,created_at,updated_at,orders_count,state,total_spent,tags,accepts_marketing_updated_at"
CUSTOMER_FIELDS = "id,accepts_marketing,created_at,updated_at,orders_count,state,total_spent,last_order_name,last_order_id,note,verified_email,tags,accepts_marketing_updated_at,marketing_opt_in_level,email_marketing_consent,sms_marketing_consent"

def order_count_filters_to_url_params(filters: OrderCountUrlParams) -> str:
    params = {}

    if filters.created_at_max:
        params["created_at_max"] = filters.created_at_max.isoformat()
    if filters.created_at_min:
        params["created_at_min"] = filters.created_at_min.isoformat()
    if filters.financial_status:
        params["financial_status"] = filters.financial_status.value
    if filters.fulfillment_status:
        params["fulfillment_status"] = filters.fulfillment_status.value
    if filters.status:
        params["status"] = filters.status.value
    if filters.updated_at_max:
        params["updated_at_max"] = filters.updated_at_max.isoformat()
    if filters.updated_at_min:
        params["updated_at_min"] = filters.updated_at_min.isoformat()

    return urlencode(params)

def order_filters_to_url_params(filters: OrderUrlParams) -> str:
    params = {}

    if filters.attribution_app_id:
        params["attribution_app_id"] = filters.attribution_app_id
    if filters.created_at_max:
        params["created_at_max"] = filters.created_at_max.isoformat()
    if filters.created_at_min:
        params["created_at_min"] = filters.created_at_min.isoformat()
    if filters.fields:
        params["fields"] = filters.fields       
    if filters.financial_status:
        params["financial_status"] = filters.financial_status.value
    if filters.fulfillment_status:
        params["fulfillment_status"] = filters.fulfillment_status.value
    if filters.ids:
        params["ids"] = filters.ids
    if filters.limit:
        params["limit"] = str(filters.limit)
    if filters.processed_at_max:
        params["processed_at_max"] = filters.processed_at_max.isoformat()
    if filters.processed_at_min:
        params["processed_at_min"] = filters.processed_at_min.isoformat()        
    if filters.since_id:
        params["since_id"] = str(filters.since_id)
    if filters.status:
        params["status"] = filters.status.value
    if filters.updated_at_max:
        params["updated_at_max"] = filters.updated_at_max.isoformat()
    if filters.updated_at_min:
        params["updated_at_min"] = filters.updated_at_min.isoformat()

    return urlencode(params)

def customer_count_filters_to_url_parms(filters: CustomerCountUrlParams) -> str:
    params = {}

    if filters.created_at_max:
        params["created_at_max"] = filters.created_at_max.isoformat()
    if filters.created_at_min:
        params["created_at_min"] = filters.created_at_min.isoformat()
    if filters.updated_at_max:
        params["updated_at_max"] = filters.updated_at_max.isoformat()
    if filters.updated_at_min:
        params["updated_at_min"] = filters.updated_at_min.isoformat()

    return urlencode(params)

def customer_search_filters_to_url_params(filters: CustomerSearchUrlParams) -> str:
    params = {}

    if filters.fields:
        params["fields"] = filters.fields
    if filters.limit:
        params["limit"] = str(filters.limit)
    if filters.order_field and filters.order_direction:
        params["order"] = filters.order_field + " " + filters.order_direction.value
    if filters.query:
        params["query"] = filters.query

    return urlencode(params)


def authenticated_api_request(
    shop_api_key: str, 
    shop_domain_name: str, 
    endpoint: str, 
    method="GET", 
    data={}
):
    url = f"https://{shop_domain_name}{endpoint}"
    headers = {
        "X-Shopify-Access-Token": shop_api_key
    }
    if method == "GET":
      response = requests.get(url, headers=headers)
    elif method == "POST":
      response = requests.post(url, headers=headers, data=data)
    elif method == "PUT":
      response = requests.put(url, headers=headers, data=data)
    elif method == "DELETE":
      response = requests.delete(url, headers=headers)
    return response.json()


def get_shop_order(shop_api_key: str, shop_domain_name: str, order_id: int, fields: str = None):
    endpoint = f"/admin/api/{SHOPIFY_API_VERSION}/orders/{order_id}.json"
    if fields:
        endpoint = f"{endpoint}?fields={fields}"
    return authenticated_api_request(shop_api_key, shop_domain_name, endpoint)


def get_shop_orders(shop_api_key: str, shop_domain_name: str, filters: OrderUrlParams):
    params = order_filters_to_url_params(filters)
    endpoint = f"/admin/api/{SHOPIFY_API_VERSION}/orders.json?{params}"
    return authenticated_api_request(shop_api_key, shop_domain_name, endpoint)


def get_shop_orders_count(shop_api_key: str, shop_domain_name: str, filters: OrderCountUrlParams):
    params = order_count_filters_to_url_params(filters)
    endpoint = f"/admin/api/{SHOPIFY_API_VERSION}/orders/count.json?{params}"
    return authenticated_api_request(shop_api_key, shop_domain_name, endpoint)


def get_shop_customer(shop_api_key: str, shop_domain_name: str, customer_id: int, fields: str = None):
    endpoint = f"/admin/api/{SHOPIFY_API_VERSION}/customers/{customer_id}.json"
    if fields:
        endpoint = f"{endpoint}?fields={fields}"
    return authenticated_api_request(shop_api_key, shop_domain_name, endpoint)


def get_shop_customers(shop_api_key: str, shop_domain_name: str, filters: CustomerSearchUrlParams):
    params = customer_search_filters_to_url_params(filters)
    endpoint = f"/admin/api/{SHOPIFY_API_VERSION}/customers/search.json?{params}"
    return authenticated_api_request(shop_api_key, shop_domain_name, endpoint)


def get_shop_customers_count(shop_api_key: str, shop_domain_name: str, filters: CustomerCountUrlParams):
    params = customer_count_filters_to_url_parms(filters)
    endpoint = f"/admin/api/{SHOPIFY_API_VERSION}/customers/count.json?{params}"
    return authenticated_api_request(shop_api_key, shop_domain_name, endpoint)
