import strawberry
from strawberry.types import Info
# from app.utility.auth_support import auth_support
# from app.utility.razorpay_client import razorpay_client
from app.resolvers.order.order_type import OrderInput, OrderResponse
from app.utility.auth_support import auth_support
from app.database import product_collection, order_collection
from datetime import datetime, timezone
# from app.database import product_collection
# import os
from bson import ObjectId

# @strawberry.type
# class OrderMutation:

#     @strawberry.mutation
#     async def create_razorpay_order(
#         self,
#         info: Info,
#         product_id: str,
#         quantity: int,
#         payment_method: str,  # "upi" / "card" / "cod"
#     ) -> RazorpayOrderResponse:
#         user_id = auth_support.get_user_from_info(info)

#         # product fetch karo
#         product = await product_collection.find_one({"_id": ObjectId(product_id)})
#         if not product:
#             raise Exception("Product nahi mila")

#         # amount calculate karo — backend pe hamesha
#         price = product.get("sale_price") or product["price"]
#         subtotal = price * quantity
#         shipping = 0 if subtotal >= 1000 else 99
#         total_amount = subtotal + shipping

#         # COD ke liye Razorpay order nahi banana
#         if payment_method == "cod":
#             # seedha order save karo DB mein
#             pass

#         # Razorpay order create karo — amount paise mein hota hai
#         razorpay_order = razorpay_client.order.create({
#             "amount": total_amount * 100,  # rupees → paise
#             "currency": "INR",
#             "payment_capture": 1,  # auto capture
#         })

#         return RazorpayOrderResponse(
#             razorpay_order_id=razorpay_order["id"],
#             amount=total_amount * 100,
#             currency="INR",
#             key_id=os.getenv("RAZORPAY_KEY_ID"),
#         )



@strawberry.type
class OrderMutation:

    @strawberry.mutation
    async def create_order(self, input: OrderInput, info: Info) -> OrderResponse:

        # 1. Token verify — sirf logged in user
        user_id = auth_support.get_user_from_info(info)
                
        # 2. Input validation
        if not input.address.full_name.strip():
            raise Exception("Full name zaroori hai")
        if not input.address.phone_num.strip():
            raise Exception("Phone number zaroori hai")
        if not input.address.street_address.strip():
            raise Exception("Street address zaroori hai")
        if not input.address.city.strip():
            raise Exception("City zaroori hai")
        if not input.address.state.strip():
            raise Exception("State zaroori hai")
        if not input.address.pin_code.strip():
            raise Exception("Pin code zaroori hai")
        if not input.address.pin_code.strip().isdigit() or len(input.address.pin_code.strip()) != 6:
            raise Exception("Pin code 6 digit ka number hona chahiye")
        if not input.address.phone_num.strip().isdigit() or len(input.address.phone_num.strip()) != 10:
            raise Exception("Phone number 10 digit ka hona chahiye")
        if input.quantity < 1:
            raise Exception("Quantity kam se kam 1 honi chahiye")
        
        
        # 3. Product check karo
        product = await product_collection.find_one(
            {"_id": ObjectId(input.product_id)}
        )
        if not product:
            raise Exception("Product nahi mila")
        if product["stock"] < input.quantity:
            raise Exception("Itna stock nahi hai")
        
        # 4. Price calculate karo
        price = product.get("sale_price") or product["price"]
        total = price * input.quantity
        
        # 5. Order number banao
        count = await order_collection.count_documents({})
        order_number = f"ORD-{datetime.now(timezone.utc).year}-{str(count + 1).zfill(4)}"
        
        shipping = 99 if  total < 1000 else 0
        
        order = {
            "order_number": order_number,
            "user_id": ObjectId(user_id),
            "items": [
                {
                    "product_id": ObjectId(input.product_id),
                    "name": product["product_name"],
                    "image": product.get("image"),
                    "price": price,
                    "quantity": input.quantity,
                }
            ],
            "subtotal": total,
            "discount": 0,
            "shipping": shipping,
            "total": total,
            "delivery_address": {
                "full_name": input.address.full_name.strip(),
                "phone_num": input.address.phone_num.strip(),
                "street_address": input.address.street_address.strip(),
                "city": input.address.city.strip(),
                "state": input.address.state.strip(),
                "pin_code": input.address.pin_code.strip(),
            },
            "payment_status": "pending",
            "status": "pending",
            "created_at": datetime.now(timezone.utc),
        }
        
        # 7. MongoDB mein save karo
        result = await order_collection.insert_one(order)
        
        # 8. Stock update karo
        await product_collection.update_one(
            {"_id": ObjectId(input.product_id)},
            {"$inc": {"stock": -input.quantity}}
        )
        
        return OrderResponse(
            order_id=str(result.inserted_id),
            order_number=order_number,
            total=total,
            message="Order successfully place ho gaya"
        )