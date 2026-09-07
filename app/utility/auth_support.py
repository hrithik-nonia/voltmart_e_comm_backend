import bcrypt


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


auth_support = AuthSupport()