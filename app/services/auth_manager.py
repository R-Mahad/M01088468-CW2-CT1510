from models.user import User


class AuthManager:
    """
    Handles registration and login.
    Uses DatabaseManager for DB access and a hasher object for password checks.
    """

    def __init__(self, db_manager, hasher):
        self.__db_manager = db_manager
        self.__hasher = hasher

    def register_user(self, username: str, plain_password: str, role: str = "user") -> bool:
        """
        Register a user.
        Returns True if successful, False if username already exists.
        """
        # Check if username exists
        existing = self.__db_manager.fetch_one(
            "SELECT username FROM users WHERE username = ?",
            (username,),
        )
        if existing is not None:
            return False

        password_hash = self.__hasher.hash_password(plain_password)

        self.__db_manager.execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role),
        )
        return True

    def login_user(self, username: str, plain_password: str) -> User | None:
        """
        Try to log in. Returns a User object if successful, otherwise None.
        """
        row = self.__db_manager.fetch_one(
            "SELECT id, username, password_hash, role FROM users WHERE username = ?",
            (username,),
        )

        if row is None:
            return None

        user_id, db_username, password_hash, role = row

        if self.__hasher.check_password(plain_password, password_hash):
            # Create and return User object (Week 11 OOP style)
            return User(db_username, password_hash, role)

        return None
