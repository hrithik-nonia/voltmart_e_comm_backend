import strawberry
from typing import Optional

# ── GraphQL Types ──────────────────────────

@strawberry.type
class UserData:
    id: str
    name: str
    email: str
    role: str
    image: Optional[str] = None

@strawberry.type
class AuthPayload:
    token: str
    message: str
    user: UserData