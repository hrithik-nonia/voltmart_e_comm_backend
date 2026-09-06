import strawberry
from app.resolvers.hello import Query

schema = strawberry.Schema(query=Query)