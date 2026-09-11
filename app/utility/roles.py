import strawberry
from enum import Enum

@strawberry.enum
class Role(Enum):
    USER = "user"
    ADMIN = "admin"
    SELLER = "seller"