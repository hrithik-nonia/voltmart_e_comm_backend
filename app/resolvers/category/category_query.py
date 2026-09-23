import strawberry
from app.database import category_collection
from app.resolvers.category.category_type import CategoryType, CategoryForAdmin
from strawberry.types import Info
from bson import ObjectId
from app.utility.auth_support import auth_support
from app.database import users_collection
from typing import Optional


# ── Query ──
@strawberry.type
class CategoryQuery:

    @strawberry.field
    async def get_category(self, info: Info) -> list[CategoryType]:
        user_id = auth_support.get_user_from_info(info)
        get_admin = await users_collection.find_one({"_id": ObjectId(user_id)})
        
        if not get_admin or get_admin["role"] not in ["admin", "superadmin"]:
            raise Exception("Tu Admin Nahi Hai")
        
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
        
    @strawberry.field
    async def get_admin_category(self, info: Info, status: Optional[str] = None) -> list[CategoryForAdmin]:

        user_id = auth_support.get_user_from_info(info)
        get_admin = await users_collection.find_one({"_id": ObjectId(user_id)})

        if not get_admin or get_admin["role"] not in ["admin", "superadmin"]:
            raise Exception("Tu Admin Nahi Hai")

        # ── Status filter ──
        match_stage = {}
        if status:
            if status not in ["active", "inactive"]:
                raise Exception("Status 'active' ya 'inactive' hona chahiye")
            match_stage["is_active"] = True if status == "active" else False

        pipeline = [
            # 0. Status filter
            {"$match": match_stage},  # ← add kiya

            # 1. Products collection se total count lo
            {
                "$lookup": {
                    "from": "products",
                    "localField": "_id",
                    "foreignField": "category_id",
                    "as": "products"
                }
            },
            # 2. Total products count karo
            {
                "$addFields": {
                    "total_products": {"$size": "$products"}
                }
            },
            # 3. Sirf zaroori fields lo
            {
                "$project": {
                    "_id": 1,
                    "name": 1,
                    "slug": 1,
                    "description": 1,
                    "icon": 1,
                    "is_active": 1,
                    "total_products": 1
                }
            }
        ]

        categories = await category_collection.aggregate(pipeline).to_list(length=None)

        result = []
        for cat in categories:
            result.append(CategoryForAdmin(
                id=str(cat["_id"]),
                name=cat["name"],
                slug=cat["slug"],
                description=cat.get("description", ""),
                icon=cat.get("icon", ""),
                total_products=cat["total_products"],
                status="Active" if cat.get("is_active") else "Inactive"
            ))

        return result