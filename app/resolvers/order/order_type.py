import strawberry
from enum import Enum

# @strawberry.type
# class RazorpayOrderResponse:
#     razorpay_order_id: str
#     amount: int
#     currency: str
#     key_id: str

@strawberry.input
class DeliveryAddressInput:
    full_name: str
    phone_num: str
    street_address: str
    city: str
    state: str
    pin_code: str
    
@strawberry.type
class DeliveryAddressResponse:
    full_name: str
    phone_num: str
    street_address: str
    city: str
    state: str
    pin_code: str


@strawberry.input
class OrderInput:
    product_id: str
    quantity: int
    address: DeliveryAddressInput
    
@strawberry.type
class OrderResponse:
    order_id: str
    order_number: str
    total: float
    message: str
    
@strawberry.type
class MyOrdersResponse:
    id: str
    order_number: str
    product_image: str
    product_name: str
    quantity: int
    total: float
    payment_status: str
    delivery_status: str
    created_at: str
    
@strawberry.type
class Amounts:
    subtotal: float
    discount: float
    shipping: float
    
@strawberry.type
class GetASingleOrder(MyOrdersResponse):
    address: DeliveryAddressResponse
    amounts: Amounts
    
    
# ── Status Enum ──
@strawberry.enum
class OrderStatus(Enum):
    ALL = "all"
    PENDING = "pending"
    CONFIRMED= "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"