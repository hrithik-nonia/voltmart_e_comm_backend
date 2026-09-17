import strawberry
from app.resolvers.order.order_type import MyOrdersResponse, OrderStatus
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
    
    
    