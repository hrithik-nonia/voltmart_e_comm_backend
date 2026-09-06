import strawberry
from enum import Enum

from app.resolvers.hello import Query

schema = strawberry.Schema(query=Query)


# ======================
@strawberry.enum
class Role(Enum):
    USER = "user"
    ADMIN = "admin"
    SELLER = "seller"