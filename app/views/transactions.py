from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models import Transaction

router = APIRouter()


@router.post("/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: Transaction,
    session: AsyncSession = Depends(get_session),
):
    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)
    return transaction


@router.get("/", response_model=list[Transaction])
async def list_transactions(
    teller_id: UUID | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Transaction)
    if teller_id:
        stmt = stmt.where(Transaction.teller_id == teller_id)

    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(
    transaction_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    tx = await session.get(Transaction, transaction_id)
    if not tx:
        raise HTTPException(404, "Transaction not found")
    return tx

@router.patch("/{transaction_id}", response_model=Transaction)
async def update_transaction(
    transaction_id: UUID,
    data: Transaction,
    session: AsyncSession = Depends(get_session),
):
    tx = await session.get(Transaction, transaction_id)
    if not tx:
        raise HTTPException(404, "Transaction not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(tx, key, value)

    await session.commit()
    await session.refresh(tx)
    return tx


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    tx = await session.get(Transaction, transaction_id)
    if not tx:
        raise HTTPException(404, "Transaction not found")

    await session.delete(tx)
    await session.commit()
