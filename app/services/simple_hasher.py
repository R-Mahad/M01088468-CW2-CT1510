import hashlib


class SimpleHasher:
    """
    Simple password hasher for learning purposes.
    (Not production-grade, but perfect for Week 11 OOP demonstration.)
    """

    def hash_password(self, plain_password: str) -> str:
        return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()

    def check_password(self, plain_password: str, stored_hash: str) -> bool:
        return self.hash_password(plain_password) == stored_hash
