import strawberry
from app.database import product_collection, cart_collection
from typing import Optional, List
from app.resolvers.product.type import ProductsResponse, Product, PaginationInfo, SingleProduct, ProductType, SpecsType, OrderProduct, CartDataResponse
from math import ceil
from bson import ObjectId
from strawberry.types import Info
from app.utility.auth_support import auth_support

@strawberry.type
class ProductQuery:

    @strawberry.field
    async def products(
        self,
        page: int = 1,
        limit: int = 10,
        category_id: Optional[str] = None, 
    ) -> ProductsResponse:
        skip = (page - 1) * limit

        match_filter = {}
        if category_id:                             
            match_filter["category"] = category_id
            
        pipeline = [
            {"$match": match_filter},
            # category collection se join
            {
                "$lookup": {
                    "from": "categories",
                    "localField": "category",
                    "foreignField": "_id",
                    "as": "category_data",
                }
            },
            {"$unwind": {"path": "$category_data", "preserveNullAndEmptyArrays": True}},
            {"$skip": skip},
            {"$limit": limit},
        ]

        raw_products = await product_collection.aggregate(pipeline).to_list(length=limit)

        total = await product_collection.count_documents(match_filter)
        total_pages = ceil(total / limit) if total > 0 else 1

        products = []
        for p in raw_products:
            cat = p.get("category_data", {})
            products.append(
                Product(
                    id=str(p["_id"]),
                    product_name=p["product_name"],
                    description=p["description"],
                    price=p["price"],
                    sale_price=p.get("sale_price"),
                    category=cat.get("name", "Unknown"),
                    category_id=str(p["category"]),
                    image=p["image"],
                )
            )
            
        return ProductsResponse(  
            data=products,
            pagination=PaginationInfo(
                page=page,
                limit=limit,
                total=total,
                has_next=page < total_pages,
            ),
        )
        
    @strawberry.field
    async def get_product_by_id(self, product_id: str) -> SingleProduct:
        product = await product_collection.find_one({"_id": ObjectId(product_id)})

        if not product:
            raise Exception("Product Nahi hai")
        
        specs = product.get("specs", {})

        return SingleProduct(
            data=ProductType(
                id=str(product["_id"]),
                product_name=product["product_name"],
                description=product.get("description", ""),
                price=product["price"],
                sale_price=product.get("sale_price"),
                stock=product.get("stock", 0),
                category=product.get("category", ""),
                image=product.get("image", ""),
                is_active=product.get("is_active", True),
                is_featured=product.get("is_featured", False),
            ),
            specs=SpecsType(
                brand=specs.get("brand", ""),
                color=specs.get("color", ""),
                warranty=specs.get("warranty", ""),
            ),
        )
        
        
    @strawberry.field
    async def get_order_product(self, info: Info, product_id: str, quantity: int) -> List[OrderProduct]:
        # token verify kiya
        user_id = auth_support.get_user_from_info(info)

        # phir product fetch karo
        product = await product_collection.find_one({"_id": ObjectId(product_id)})
        
        if not product:
            raise Exception("Product Nahi hai")
        
        total_price = product["price"] * quantity  

        return OrderProduct(
            id=str(product["_id"]),        
            name=product["product_name"],
            image=product["image"],
            quantity=quantity,
            price=product["price"],
            total_price=total_price,         
        )
        
    @strawberry.field
    async def get_cart_data(self, info: Info)-> List[CartDataResponse]:
        # token verify kiya
        user_id = auth_support.get_user_from_info(info)
        
        print(user_id)
        
        # create pipeline 
        pipeline = [
            # Step 1 — user ke cart items
            {"$match": {"user_id": user_id}},
            
            # product_id string → ObjectId
            {"$addFields": {"product_id_obj": {"$toObjectId": "$product_id"}}},
            
            # Step 2 — product_id se product join kiya
            {
                "$lookup": {
                    "from": "products",
                    "localField": "product_id_obj",
                    "foreignField": "_id", 
                    "as": "product_data",
                }
            },
            {"$unwind": "$product_data"},
        ]
        
        cart_items = await cart_collection.aggregate(pipeline).to_list(length=100)
        
        return [
            CartDataResponse(
                cart_id=str(item["_id"]),
                product_id=str(item["product_id"]),
                image=item["product_data"]["image"],
                product_name=item["product_data"]["product_name"],
                in_stock=item["product_data"]["stock"] > 0,
                description=item["product_data"]["description"],
                sale_price=item["product_data"].get("sale_price"),
                price=item["product_data"]["price"],
                quantity= item["quantity"]
            )
            for item in cart_items
        ]