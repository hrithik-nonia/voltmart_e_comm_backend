import strawberry
from typing import Optional

@strawberry.type
class SpecsType:
    brand: str
    color: str
    warranty: str

@strawberry.type
class ProductType:
    id: str
    product_name: str
    description: str
    price: float
    sale_price: Optional[float]
    stock: int
    category: str
    image: str
    is_active: bool
    is_featured: bool

@strawberry.input
class SpecsInput:
    brand: str = ""
    color: str = ""
    warranty: str = ""

@strawberry.input
class ProductInput:
    product_name: str
    price: float
    stock: int
    category: str
    image: str
    description: str = ""
    sale_price: Optional[float] = None
    specs: SpecsInput = strawberry.field(default_factory=SpecsInput)
    is_active: bool = True
    is_featured: bool = False