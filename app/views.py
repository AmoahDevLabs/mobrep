from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from .models import Teller, User, Transaction


async def create_teller(session: AsyncSession, teller: Teller):
    session.add(teller)
    await session.commit()
    await session.refresh(teller)
    return teller


async def create_user(session: AsyncSession, user: User):
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def log_transaction(
    session: AsyncSession, transaction: Transaction
):
    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)
    return transaction


async def list_transactions(
    session: AsyncSession, teller_id: UUID | None = None
):
    stmt = select(Transaction)
    if teller_id:
        stmt = stmt.where(Transaction.teller_id == teller_id)

    result = await session.execute(stmt)
    return result.scalars().all()
