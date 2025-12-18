from __future__ import annotations

from typing import Optional, List
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import func

from .enums import UserStatus



def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# =========================
# Teller
# =========================
class Teller(SQLModel, table=True):
    __tablename__ = "tellers"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    name: str = Field(nullable=False)
    phone: str = Field(nullable=False)
    address: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)

    created_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
    )

    transactions: List[Transaction] = Relationship(
        back_populates="teller"
    )


# =========================
# User
# =========================
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    name: str = Field(nullable=False)
    phone: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True, index=True)
    status: UserStatus = Field(nullable=False)

    created_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
    )


# =========================
# Transaction (Audit Log)
# =========================
class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    teller_id: UUID = Field(
        foreign_key="tellers.id",
        nullable=False,
        index=True,
    )

    expected_amount: float = Field(nullable=False)
    actual_amount: float = Field(nullable=False)

    remarks: Optional[str] = Field(default=None)

    timestamp: datetime = Field(
        default_factory=utc_now,
        nullable=False,
        index=True,
    )

    teller: Optional[Teller] = Relationship(
        back_populates="transactions"
    )
