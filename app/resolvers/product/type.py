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
    
    
@strawberry.type
class CartResponse:
    message: str
    
@strawberry.type
class OrderProduct:
    id:str
    name: str
    image: str
    quantity: int
    price: float
    total_price: float
    
    
@strawberry.type
class CartDataResponse:
    cart_id: str
    product_id: str
    image: str
    product_name: str
    in_stock: bool
    description: str
    sale_price: Optional[float]
    price: float
    quantity: int
    
    
@strawberry.type
class AdminProductResponse:
    id: str
    image: str
    product_name: str
    sku: str
    created_at: str
    price: float
    stock: int
    is_active: bool
    specs: SpecsType
    
    
@strawberry.type
class AdminProductsResponse:
    products: list[AdminProductResponse]
    pagination: PaginationInfo
    
    
@strawberry.type
class InventoryStats:
    total_products: int
    active_products: int
    low_stock: int
    out_of_stock: int
    