from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models import User

router = APIRouter()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: User,
    session: AsyncSession = Depends(get_session),
):
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.get("/", response_model=list[User])
async def list_users(
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(User))
    return result.scalars().all()


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.patch("/{user_id}", response_model=User)
async def update_user(
    user_id: UUID,
    data: User,
    session: AsyncSession = Depends(get_session),
):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    await session.commit()
    await session.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    await session.delete(user)
    await session.commit()
