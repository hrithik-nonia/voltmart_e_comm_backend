import strawberry
from app.database import users_collection
from app.utility.auth_support import auth_support
from app.utility.jwt_support import create_token
from app.utility.auth_model import AuthPayload, UserData
    

# ── Mutation ──────────────────────────────
@strawberry.type
class AdminAuth:

    @strawberry.mutation
    async def login(self, email: str, password: str) -> AuthPayload:

        # 1. Email se admin dhundo
        user = await users_collection.find_one({"email": email})
        if not user:
            raise Exception("Email ya password galat hai")

        # 2. Password verify karo
        is_valid = auth_support.verify_pass(password, user["password"])
        if not is_valid:
            raise Exception("Email ya password galat hai")

        # 3. Active check
        if not user.get("is_active", True):
            raise Exception("Account disabled hai")

        # 4. Token banao
        token = create_token(str(user["_id"]), user["role"])
        
        # 5. UserData object banao ✅
        user_data = UserData(
          id=str(user["_id"]),        # ← ObjectId → string
          name=user["name"],
          email=user["email"],
          role=user["role"],
          image=user.get("image")     # ← None bhi ho sakta hai
        )

        return AuthPayload(
            token=token,
            message="Login successful",
            user= user_data
        )