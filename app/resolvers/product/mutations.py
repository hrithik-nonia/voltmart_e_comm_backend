import strawberry
from pydantic import ValidationError
from app.resolvers.product.type import ProductType, ProductInput
from app.utility.product_model import ProductModel, SpecsModel
from app.database import db

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
        result = await db.products.insert_one(doc)

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