import strawberry
from app.resolvers.order.order_type import MyOrdersResponse, OrderStatus, GetASingleOrder, DeliveryAddressResponse, Amounts
from strawberry.types import Info
from app.utility.auth_support import auth_support
from app.database import order_collection
from bson import ObjectId
from typing import Optional


@strawberry.type
class OrderQuery:
  
  @strawberry.field
  async def get_orders(
      self,
      info: Info,
      status: Optional[OrderStatus]= None
    ) -> list[MyOrdersResponse]:
    
    # 1. Token se user_id
    user_id = auth_support.get_user_from_info(info)
    
    # 2. Filter banao
    query = {"user_id": ObjectId(user_id)}
    if status and status != "all":
        query["status"] = status.value
        
    # 3. Orders fetch karo
    orders = await order_collection.find(query).to_list(length=None)
        
    # 4. Response banao
    result = []
    
    for order in orders:
      result.append(MyOrdersResponse(
          id=str(order["_id"]),
          product_id=str(order["items"][0]["product_id"]),
          order_number=order["order_number"],
          product_image=order["items"][0].get("image") or "",
          product_name=order["items"][0]["name"],
          quantity=order["items"][0]["quantity"],
          total=order["total"],
          payment_status=order["payment_status"],
          delivery_status=order["status"],
          created_at=str(order["created_at"])
      ))
    
   
    return result
  
  @strawberry.field
  async def get_order_by_id(
      self,
      order_id: str,
      info: Info
  ) -> GetASingleOrder:

      # 1. Token se user_id
      user_id = auth_support.get_user_from_info(info)
      

      # 2. Filter
      query = {
          "_id": ObjectId(order_id),
          "user_id": ObjectId(user_id)
      }

      # 3. Order fetch
      order = await order_collection.find_one(query)

      if not order:
          raise Exception("Order not found")

      item = order["items"][0]
      address = order["delivery_address"]

      return GetASingleOrder(
          id=str(order["_id"]),
          order_number=order["order_number"],
          product_image=item.get("image") or "",
          product_name=item["name"],
          quantity=item["quantity"],
          total=order["total"],
          payment_status=order["payment_status"],
          delivery_status=order["status"],
          created_at=str(order["created_at"]),

          address=DeliveryAddressResponse(
              full_name=address["full_name"],
              phone_num=address["phone_num"],
              street_address=address["street_address"],
              city=address["city"],
              state=address["state"],
              pin_code=address["pin_code"],
          ),

          amounts=Amounts(
              subtotal=order["subtotal"],
              discount=order["discount"],
              shipping=order["shipping"],
          )
      )
      
      
      
      