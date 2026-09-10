from pydantic import BaseModel, field_validator, model_validator
from typing import Optional

class SpecsModel(BaseModel):
    brand: str = ""
    color: str = ""
    warranty: str = ""

class ProductModel(BaseModel):
    product_name: str
    description: str = ""
    price: float
    sale_price: Optional[float] = None
    stock: int
    category: str
    image: str
    specs: SpecsModel = SpecsModel()
    is_active: bool = True
    is_featured: bool = False

    @field_validator("product_name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Product name cannot be empty")
        return v.strip()

    @field_validator("price", "stock")
    @classmethod
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Must be greater than 0")
        return v

    @field_validator("sale_price")
    @classmethod
    def sale_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Sale price must be positive")
        return v

    @model_validator(mode="after")
    def sale_less_than_price(self):
        if self.sale_price and self.sale_price >= self.price:
            raise ValueError("Sale price must be less than original price")
        return self