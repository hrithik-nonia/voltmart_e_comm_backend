import strawberry
from enum import Enum

from app.resolvers.hello import Query as HelloQuery
from app.resolvers.admin.admin_auth import AdminAuth
from app.resolvers.product.queries import ProductQuery
from app.resolvers.product.mutations import ProductMutation
from app.resolvers.user.user_query import UserQuery
from app.resolvers.user.user_mutation import UserMutation
from app.resolvers.category.category_query import CategoryQuery



# ✅ Saari queries merge
@strawberry.type
class Query(HelloQuery, ProductQuery, UserQuery, CategoryQuery):
    pass


# ✅ Saare mutations merge
@strawberry.type
class Mutation(AdminAuth, ProductMutation, UserMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)


