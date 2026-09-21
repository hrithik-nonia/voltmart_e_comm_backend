import strawberry
from typing import Optional

@strawberry.type
class CategoryType:
    id: str
    name: str
    slug: str
    description: str
    icon: str

@strawberry.input
class CreateCategory:
    name: str
    description: Optional[str]
    is_active: bool
    
@strawberry.type
class CreateCategoryResponse:
  message: str