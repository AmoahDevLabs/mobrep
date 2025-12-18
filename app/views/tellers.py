from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models import Teller

router = APIRouter()


@router.post("/", response_model=Teller, status_code=status.HTTP_201_CREATED)
async def create_teller(
    teller: Teller,
    session: AsyncSession = Depends(get_session),
):
    session.add(teller)
    await session.commit()
    await session.refresh(teller)
    return teller


@router.get("/", response_model=list[Teller])
async def list_tellers(
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Teller))
    return result.scalars().all()


@router.get("/{teller_id}", response_model=Teller)
async def get_teller(
    teller_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    teller = await session.get(Teller, teller_id)
    if not teller:
        raise HTTPException(404, "Teller not found")
    return teller


@router.patch("/{teller_id}", response_model=Teller)
async def update_teller(
    teller_id: UUID,
    data: Teller,
    session: AsyncSession = Depends(get_session),
):
    teller = await session.get(Teller, teller_id)
    if not teller:
        raise HTTPException(404, "Teller not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(teller, key, value)

    await session.commit()
    await session.refresh(teller)
    return teller


@router.delete("/{teller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teller(
    teller_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    teller = await session.get(Teller, teller_id)
    if not teller:
        raise HTTPException(404, "Teller not found")

    await session.delete(teller)
    await session.commit()
