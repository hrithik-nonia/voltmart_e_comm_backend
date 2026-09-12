import strawberry
from app.database import category_collection


# ── Category Type ──
@strawberry.type
class CategoryType:
    id: str
    name: str
    slug: str
    description: str
    icon: str


# ── Query ──
@strawberry.type
class CategoryQuery:

    @strawberry.field
    async def get_category() -> list[CategoryType]:
        categories = await category_collection.find(
            {"is_active": True}
        ).to_list(length=None)

        return [
            CategoryType(
                id=str(category["_id"]),
                name=category["name"],
                slug=category["slug"],
                description=category["description"],
                icon=category["icon"],
            )
            for category in categories
        ]