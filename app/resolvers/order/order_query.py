import strawberry
from app.resolvers.order.order_type import MyOrdersResponse, OrderStatus, GetASingleOrder, DeliveryAddressResponse, Amounts, DashboardStats, CustomerStats
from strawberry.types import Info
from app.utility.auth_support import auth_support
from app.database import order_collection, product_collection, users_collection
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
          product_id=str(item["product_id"]),
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
      
      
  @strawberry.field
  async def get_dashboard_stats(self) -> DashboardStats:

    pipeline = [
        {
            "$facet": {
                # Total fulfillment — delivered orders count
                "total_fulfillment": [
                    {"$match": {"status": "delivered"}},
                    {"$count": "count"}
                ],
                # Total revenue — delivered orders ka total
                "total_revenue": [
                    {"$match": {"status": "delivered"}},
                    {"$group": {"_id": None, "total": {"$sum": "$total"}}}
                ],
                "total_orders": [          
                    {"$count": "count"}
                ],
            }
        }
    ]

    order_result = await order_collection.aggregate(pipeline).to_list(length=1)
    order_data = order_result[0] if order_result else {}

    fulfillment_data = order_data.get("total_fulfillment", [])
    total_fulfillment = fulfillment_data[0].get("count", 0) if fulfillment_data else 0

    revenue_data = order_data.get("total_revenue", [])
    total_revenue = revenue_data[0].get("total", 0.0) if revenue_data else 0.0

    # ← Yeh 2 lines missing hain
    total_products = await product_collection.count_documents({})
    total_customers = await users_collection.count_documents({"role": "user"})
    
    orders_data = order_data.get("total_orders", [])
    total_orders = orders_data[0].get("count", 0) if orders_data else 0

    return DashboardStats(
        total_revenue=total_revenue,
        total_fulfillment=total_fulfillment,
        total_orders=total_orders,
        total_products=total_products,
        total_customers=total_customers
    )
    
    
  @strawberry.field
  async def get_customer_stats(self) -> CustomerStats:

    pipeline = [
        {
            "$group": {
                "_id": None,
                "total_customers": {
                    "$sum": {"$cond": [{"$eq": ["$role", "user"]}, 1, 0]}
                },
                "active_users": {
                    "$sum": {
                        "$cond": [
                            {"$and": [
                                {"$eq": ["$role", "user"]},
                                {"$eq": ["$is_active", True]}
                            ]}, 1, 0
                        ]
                    }
                },
                "admin_users": {
                    "$sum": {"$cond": [{"$eq": ["$role", "admin"]}, 1, 0]}
                },
                "inactive_users": {
                    "$sum": {
                        "$cond": [
                            {"$and": [
                                {"$eq": ["$role", "user"]},
                                {"$eq": ["$is_active", False]}
                            ]}, 1, 0
                        ]
                    }
                },
            }
        }
    ]

    result = await users_collection.aggregate(pipeline).to_list(length=1)
    data = result[0] if result else {}

    return CustomerStats(
        total_customers=data.get("total_customers", 0),
        active_users=data.get("active_users", 0),
        admin_users=data.get("admin_users", 0),
        inactive_users=data.get("inactive_users", 0)
    )
    