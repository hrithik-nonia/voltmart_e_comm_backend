import strawberry
from app.resolvers.product.type import ProductType
from app.database import db

@strawberry.type
class ProductQuery:

    @strawberry.field
    async def get_products(self) -> list[ProductType]:
        products = await db.products.find().to_list(100)

        return [
            ProductType(
                id=str(p["_id"]),
                product_name=p["product_name"],
                description=p.get("description", ""),
                price=p["price"],
                sale_price=p.get("sale_price"),
                stock=p["stock"],
                category=p.get("category", ""),
                image=p["image"],
                is_active=p["is_active"],
                is_featured=p["is_featured"],
            )
            for p in products
        ]