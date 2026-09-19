import bcrypt
from app.utility.jwt_support import verify_token


class AuthSupport:

    def hashed_pass(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        return hashed_password.decode("utf-8")
    
    def verify_pass(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(
            plain.encode("utf-8"),
            hashed.encode("utf-8")
        )
        
    # for graphQl end point
    def get_user_from_info(self, info) -> str:
        request = info.context["request"]
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            raise Exception("Token missing — Login karo")
        
        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get("id")
        
        if not user_id:
            raise Exception("Invalid token")
        
        return user_id
    


auth_support = AuthSupport()