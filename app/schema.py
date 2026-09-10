import strawberry
from enum import Enum

from app.resolvers.hello import Query as HelloQuery
from app.resolvers.admin.admin_auth import AdminAuth
from app.resolvers.product.queries import ProductQuery
from app.resolvers.product.mutations import ProductMutation
from app.resolvers.user.user_query import UserQuery


# ✅ Saari queries merge
@strawberry.type
class Query(HelloQuery, ProductQuery, UserQuery):
    pass


# ✅ Saare mutations merge
@strawberry.type
class Mutation(AdminAuth, ProductMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)


# ======================
@strawberry.enum
class Role(Enum):
    USER = "user"
    ADMIN = "admin"
    SELLER = "seller"