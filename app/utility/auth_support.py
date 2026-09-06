import bcrypt


class AuthSupport:

    def hashed_pass(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        return hashed_password.decode("utf-8")


auth_support = AuthSupport()