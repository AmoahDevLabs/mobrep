import enum


class UserStatus(str, enum.Enum):
    Admin = "admin"
    Manager = "manager"
    Coordinator = "coordinator"