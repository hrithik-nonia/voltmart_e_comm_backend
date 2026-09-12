import strawberry
from app.database import product_collection
from typing import Optional
from app.resolvers.product.type import ProductsResponse, Product, PaginationInfo
from math import ceil

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
            
        return ProductsResponse(      # yeh missing tha
            data=products,
            pagination=PaginationInfo(
                page=page,
                limit=limit,
                total=total,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_prev=page > 1,
            ),
        )