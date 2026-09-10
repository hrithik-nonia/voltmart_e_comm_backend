import strawberry
from typing import Optional
from strawberry.types import Info
from app.database import users_collection
from app.utility.jwt_support import verify_token
from bson import ObjectId


# ── User Type ──
@strawberry.type
class UserType:
    id: str
    name: str
    email: str
    role: str
    image: Optional[str] = None
    is_active: bool
    


# ── Query ──
@strawberry.type
class UserQuery:

    @strawberry.field
    async def me(self, info: Info) -> UserType:

        # 1. Header se token nikalo
        request = info.context["request"]
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise Exception("Token nahi mila")

        token = auth_header.split(" ")[1]

        # 2. Token verify karo
        payload = verify_token(token)

        # 3. MongoDB se user dhundo
        user = await users_collection.find_one(
            {"_id": ObjectId(payload["id"])}
        )

        if not user:
            raise Exception("User nahi mila")

        return UserType(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            role=user["role"],
            image=user.get("image"),
            is_active=user["is_active"],
        )