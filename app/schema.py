import strawberry
from enum import Enum

from app.resolvers.hello import Query
from app.resolvers.admin.admin_auth import AdminAuth

schema = strawberry.Schema(query=Query,mutation=AdminAuth )


# ======================
@strawberry.enum
class Role(Enum):
    USER = "user"
    ADMIN = "admin"
    SELLER = "seller"