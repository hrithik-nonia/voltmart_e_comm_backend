import strawberry
from typing import Optional, List

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

@strawberry.type
class Product:
    id: str
    product_name: str
    description: str
    sale_price: Optional[float]
    price: float
    category_id: str
    category: str 
    image: str

@strawberry.type
class PaginationInfo:
    page: int
    limit: int
    total: int
    has_next: bool

@strawberry.type
class ProductsResponse:
    data: List[Product]
    pagination: PaginationInfo
    
@strawberry.type
class SingleProduct:
    data: ProductType
    specs: SpecsType