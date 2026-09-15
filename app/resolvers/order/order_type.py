import strawberry

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
    