from enum import StrEnum

class UserRole(StrEnum):
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"