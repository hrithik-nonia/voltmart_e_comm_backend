import strawberry
from pydantic import ValidationError
from app.resolvers.product.type import ProductType, ProductInput, CartResponse
from app.utility.product_model import ProductModel, SpecsModel
from app.database import product_collection, cart_collection
from bson import ObjectId
from strawberry.types import Info
from app.utility.jwt_support import verify_token


@strawberry.type
class ProductMutation:

    @strawberry.mutation
    async def create_product(self, input: ProductInput) -> ProductType:

        # Pydantic se validate
        try:
            validated = ProductModel(
                product_name=input.product_name,    
                description=input.description,
                price=input.price,
                sale_price=input.sale_price,
                stock=input.stock,
                category=input.category,
                image=input.image,
                is_active=input.is_active,
                is_featured=input.is_featured,
                specs=SpecsModel(
                    brand=input.specs.brand,
                    color=input.specs.color,
                    warranty=input.specs.warranty,
                ),
            )
        except ValidationError as e:
            raise Exception(str(e))

        # MongoDB mein save
        doc = validated.model_dump()
        result = await product_collection.insert_one(doc)

        return ProductType(
            id=str(result.inserted_id),
            product_name=validated.product_name,
            description=validated.description,
            price=validated.price,
            sale_price=validated.sale_price,
            stock=validated.stock,
            category=validated.category,
            image=validated.image,
            is_active=validated.is_active,
            is_featured=validated.is_featured,
        )
        
    
    @strawberry.mutation
    async def create_cart_data(self, info: Info, product_id: str, quantity: int = 1) -> CartResponse:
        # request se token lo
        request = info.context["request"]
        auth_header = request.headers.get("Authorization")
        
        
        if not auth_header or not auth_header.startswith("Bearer "):
            raise Exception("Token missing")
        
        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get("id") 
        
        if not user_id:
            raise Exception("Invalid token")

        product = await product_collection.find_one({"_id": ObjectId(product_id)})
        
        if not product:
            raise Exception("Product Does Not Exist")
        
        is_product_in_cart = await cart_collection.find_one({
            "product_id": product_id,
            "user_id": user_id,
        })
        
        if is_product_in_cart:
            await cart_collection.update_one(
                {"product_id": product_id, "user_id": user_id},
                {"$inc": {"quantity": quantity}}
            )
            return CartResponse(message="Cart Updated Successfully")

        cart_item = {
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity,
        }
        
        await cart_collection.insert_one(cart_item)
        return CartResponse(message="Added To Cart Successfully")